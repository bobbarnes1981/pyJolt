import wx

class GlobalControllerOptions(wx.Dialog):

    def __init__(self, *args, **kw):
        super(GlobalControllerOptions, self).__init__(*args, **kw)

        colOffset = 205

        self.cyls = [
            '4',
            '6',
            '8'
        ]

        self.cylLabel = wx.StaticText(self, -1, label='Number of Cylinders', pos=(5,10))
        self.cylCombo = wx.ComboBox(self, -1, value=self.cyls[0], pos=(colOffset,5), choices=self.cyls, style=wx.CB_READONLY)

        self.crankLabel = wx.StaticText(self, -1, label='Cranking Advance', pos=(5,45))
        self.crankSpin = wx.SpinCtrl(self, -1, pos=(colOffset,40), min=0, max=59, initial=0)

        self.trigLabel = wx.StaticText(self, -1, label='Trigger Offset', pos=(5,75))
        self.trigSpin = wx.SpinCtrl(self, -1, pos=(colOffset,70), min=0, max=59, initial=0)

        self.filterLabel = wx.StaticText(self, -1, label='EDIS PIP Filter Level', pos=(5,105))
        self.filterSpin = wx.SpinCtrl(self, -1, pos=(colOffset,100), min=0, max=1000, initial=0)

        self.readButton = wx.Button(self, -1, label='Read Options', pos=(100,130))
        self.writeButton = wx.Button(self, -1, label='Write Options', pos=(200,130))

        self.okButton = wx.Button(self, -1, label='OK', pos=(200,165))

