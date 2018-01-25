
class Configuration():

    def __init__(self):
        self.mapBins = [20,30,40,50,60,70,80,90,100,110]
        self.rpmBins = [5,10,15,20,25,30,35,40,50,60]
        self.advance = [[24,24,29,34,37,41,44,48,48,48],
            [21,21,26,31,34,38,41,45,45,45],
            [19,19,24,29,32,36,39,43,43,43],
            [17,17,22,27,30,34,37,41,41,41],
            [15,15,20,25,28,32,35,39,39,39],
            [13,13,18,23,26,30,33,37,37,37],
            [11,11,16,21,24,28,31,35,35,35],
            [9,9,14,19,22,26,29,33,33,33],
            [8,8,13,18,21,25,28,32,32,32],
            [8,8,13,18,21,25,28,32,32,32]]
        self.correctionBins = [0,0,0,0,0,0,0,0,0,0]
        self.correctionValues = [0,0,0,0,0,0,0,0,0,0]
        self.correctionPeakHold = 0
        self.userOut = [UserOut(1, 0, 10),
            UserOut(1, 0, 10),
            UserOut(1, 0, 10),
            UserOut(1, 0, 10)]
        self.shiftLight = 55
        self.revLimit = 60

    def save(self, filename):
        pass

    def load(self, filename):
        pass

class UserOut():

    def __init__(self, type, mode, value):
        self.type = type
        self.mode = mode
        self.value = value

