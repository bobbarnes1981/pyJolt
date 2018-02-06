import wx
import serial

class AuxiliaryInputOptions(wx.Dialog):

    def __init__(self, *args, **kw):
        super(AuxiliaryInputOptions, self).__init__(*args, **kw)

    def setCommunication(self, coms):
        self.coms = coms

    def readCalibration(self):
        calibration = None
        try:
            calibration = self.coms.getAuxiliaryCalibration()
        except serial.SerialException, sException:
            wx.MessageDialog(self, sException.strerror, 'Error', wx.OK).ShowModal()
        if calibration:
            self.setCalibration(calibration)

    def setCalibration(self, calibration):
        #TODO: set ui controls from calibration
        pass

#    def onReadButton(self, commandEvent):
#        self.readCalibration()

#    def onWriteButton(self, commandEvent):
#        self.coms.updateAuxiliaryCalibration()

    def onOkButton(self, commandEvent):
        self.Hide()

    def ShowModal(self):
        self.readCalibration()
        return super(AuxiliaryInputOptions, self).ShowModal()


