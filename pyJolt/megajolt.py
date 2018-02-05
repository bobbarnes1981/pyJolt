import serial

class Configuration():

    def __init__(self):
        self.cylinders = 4
        self.mapBins = [10,20,30,40,50,60,70,80,90,100]
        self.rpmBins = [5,15,25,35,45,55,65,75,85,95]
        self.advance = [
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
        ]
        self.correctionBins = [0,0,0,0,0,0,0,0,0,0]
        self.correctionValues = [0,0,0,0,0,0,0,0,0,0]
        self.correctionPeakHold = 0
        self.userOut = [
            UserOut(1, 0, 10),
            UserOut(1, 0, 10),
            UserOut(1, 0, 10),
            UserOut(1, 0, 10)
        ]
        self.shiftLight = 55 
        self.revLimit = 60
        self.dirty = False

    def save(self, filename):
        data = "cylinders={0}\r\n".format(self.cylinders)
        data += "mapBins={0}\r\n".format(','.join(str(x) for x in self.mapBins))
        data += "rpmBins={0}\r\n".format(','.join(str(x) for x in self.rpmBins))
        for i in range(0, 10):
            data += "advance{0}={1}\r\n".format(str(i), ','.join(str(x) for x in self.advance[i]))
        data += "correctionBins={0}\r\n".format(','.join(str(x) for x in self.correctionBins))
        data += "correctionValues={0}\r\n".format(','.join(str(x) for x in self.correctionValues))
        data += "correctionPeakHold={0}\r\n".format(self.correctionPeakHold)
        for i in range(0, 4):
            u = self.userOut[i]
            data += "userOutType{0}={1}\r\nuserOutMode{0}={2}\r\nuserOutValue{0}={3}\r\n".format(str(i), str(u.type), str(u.mode), str(u.value))
        data += "shiftLight={0}\r\n".format(self.shiftLight)
        data += "revLimit={0}\r\n".format(self.revLimit)
        with open(filename, 'w') as f:
            f.write(data)

    def load(self, filename):
        with open(filename, 'r') as f:
            data = f.read()
        lines = data.split('\r\n')
        for line in lines:
            if not line:
                continue
            (k,v) = line.split('=')
            if k in ['cylinders', 'correctionPeakHold', 'shiftLight', 'revLimit']:
                self.setConfigValue(k, v)
            elif k in ['mapBins', 'rpmBins', 'correctionBins', 'correctionValues']:
                self.setConfigList(k, v)
            elif k in ['advance0', 'advance1', 'advance2', 'advance3', 'advance4', 'advance5', 'advance6', 'advance7', 'advance8', 'advance9']:
                self.setConfigListList(k, v)
            elif k in ['userOutType0', 'userOutMode0', 'userOutValue0', 'userOutType1', 'userOutMode1', 'userOutValue1','userOutType2', 'userOutMode2', 'userOutValue2','userOutType3', 'userOutMode3', 'userOutValue3']:
                self.setUserOut(k, v)
            else:
                raise Exception('failed to load line: ' + line)

    def setConfigValue(self, k, v):
        setattr(self, k, int(v))

    def setConfigList(self, k, v):
        l = v.split(',')
        l = [ int(i) for i in l ]
        setattr(self, k, l)

    def setConfigListList(self, k, v):
        num = int(k[-1:])
        k = k[:-1]
        l = v.split(',')
        l = [ int(i) for i in l ]
        attr = getattr(self, k)
        attr[num] = l
        setattr(self, k, attr)

    def setUserOut(self, k, v):
        num = int(k[-1:])
        prop = k[7:-1].lower()
        k = k[:7]
        attr = getattr(self, k)
        setattr(attr[num], prop, int(v))
        setattr(self, k, attr)

class GlobalConfiguration():

    def __init__(self):
        pass

class UserOut():

    def __init__(self, type, mode, value):
        self.type = type
        self.mode = mode
        self.value = value

class Communication():

    def __init__(self, comPort):
        self.comPort = comPort
        self.baudRate = 38400
        self.byteSize = 8
        self.parity = serial.PARITY_NONE
        self.stopBits = 1

    def makeRequest(self, char, length):
        with serial.Serial(self.comPort, self.baudRate, bytesize=self.byteSize, parity=self.parity, stopbits=self.stopBits) as ser:
            ser.write(char)
            return ser.read(length)

    def getVersion(self):
        res = self.makeRequest(b'V', 3)
        return '{0}.{1}.{2}'.format(res[0], res[1], res[2])

    def getState(self):
        res = self.makeRequest(b'S', 9)
        state = State()
        state.advance = res[0]
        state.rpm = (res[1]<<8)|(res[2]) # High byte | low byte
        state.rpmBin = res[3]>>4 # high 4 bits
        state.loadBin = res[3]|0x0F # low 4 bits
        state.load = res[4]
        state.userOut = [
            (res[5]>>0)|0x01 == 0x01,
            (res[5]>>1)|0x01 == 0x01,
            (res[5]>>2)|0x01 == 0x01,
            (res[5]>>3)|0x01 == 0x01,
        ]
        state.revLimit = (res[5]>>4)|0x01 == 0x01
        state.shiftLight = (res[5]>>5)|0x01 == 0x01
        state.config = 0 if (res[5]>>7)|0x01 == 0x01 else 1
        state.aux = res[6]
        state.correctionBin = res[7]
        state.correctionDegrees = res[8]
        return state

    def getIgnitionConfiguration(self):
        #TODO: get real configuration
        return Configuration()

    def updateIgnitionConfiguration(self):
        pass

    def updateIgnitionCell(self, rpmLoadBin, advance):
        pass

    def writeIgnitionConfiguration(self):
        pass

    def getLoadCalibration(self):
        return None

    def udpdateLoadCalibration(self, data):
        pass

    def readLoadADC(self):
        return None

    def getAuxiliaryCalibration(self):
        return None

    def updateAuxiliaryCalibration(self):
        pass

    def getGlobalConfiguration(self):
        res = self.makeRequest(b'g', 64)
        config = GlobalConfiguration()
        #TODO: load to object
        return config

    def updateGlobalConfiguration(self, cylinders, pipNoiseFilterLevel, crankingAdvance, triggerWheelOffset):
        pass

class State():

    def __init__(self):
        self.advance = 0
        self.rpm = 0
        self.rpmBin = 0
        self.loadBin = 0
        self.load = 0
        self.userOut = [
            False, False, False, False
        ]
        self.RevLimit = False
        self.shiftLight = False
        self.config = 0
        self.aux = 0
        self.correctionBin = 0
        self.correctionDegrees = 0

