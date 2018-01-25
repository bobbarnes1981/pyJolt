
class Configuration():

    def __init__(self):
        self.cylinders = 0
        self.mapBins = [0,0,0,0,0,0,0,0,0,0]
        self.rpmBins = [0,0,0,0,0,0,0,0,0,0]
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
            UserOut(0, 0, 0),
            UserOut(0, 0, 0),
            UserOut(0, 0, 0),
            UserOut(0, 0, 0)
        ]
        self.shiftLight = 0
        self.revLimit = 0

    def save(self, filename):
        data = "cylinders={0}\r\n".format(self.cylinders)
        data += "mapBins={0}\r\n".format(','.join(str(x) for x in self.mapBins))
        data += "rpmBins={0}\r\n".format(','.join(str(x) for x in self.rpmBins))
        for i in range(0, 10):
            data += "advance{0}={1}\r\n".format(str(i), ','.join(str(x) for x in self.advance[i]))
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
        setattr(attr[num], prop, v)
        setattr(self, k, attr)

class UserOut():

    def __init__(self, type, mode, value):
        self.type = type
        self.mode = mode
        self.value = value

