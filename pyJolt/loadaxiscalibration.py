import wx

class LoadAxisCalibration(wx.Dialog):

    def __init__(self, *args, **kw):
        super(LoadAxisCalibration, self).__init__(*args, **kw)

    def setCommunication(self, coms):
        self.coms = coms

    def readCalibration(self):
        calibration = None
        try:
            calibration = self.coms.getLoadAxisCalibration()
        except serial.SerialException, sException:
            wx.MessageDialog(self, sException.strerror, 'Error', wx.OK).ShowModal()
        self.setCalibration(calibration)

    def setCalibration(self, calibration):
        #TODO: set ui controls from calibration
        pass

#    def onReadButton(self, commandEvent):
#        self.readCalibration()

#    def onWriteButton(self, commandEvent):
#        self.coms.updateLoadAxisCalibration()

    def onOkButton(self, commandEvent):
        self.Hide()

    def ShowModal(self):
        self.readCalibration()
        return super(LoadAxisCalibration, self).ShowModal()

