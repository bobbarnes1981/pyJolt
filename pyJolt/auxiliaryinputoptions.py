import wx
import serial

class AuxiliaryInputOptions(wx.Dialog):

    def __init__(self, *args, **kw):
        super(AuxiliaryInputOptions, self).__init__(*args, **kw)

    def setCommunication(self, coms):
        self.coms = coms

    def readOptions(self):
        options = None
        try:
            options = self.coms.getAuxiliaryInputOptions()
        except serial.SerialException, sException:
            wx.MessageDialog(self, sException.strerror, 'Error', wx.OK).ShowModal()
        self.setOptions(options)

    def setOptions(self, options):
        #TODO: set ui controls from options
        pass

#    def onReadButton(self, commandEvent):
#        self.readOptions()

#    def onWriteButton(self, commandEvent):
#        self.coms.updateAuxiliaryInputOptions()

    def onOkButton(self, commandEvent):
        self.Hide()

    def ShowModal(self):
        self.readOptions()
        return super(AuxiliaryInputOptions, self).ShowModal()


