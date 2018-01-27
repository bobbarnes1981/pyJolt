import wx

class GlobalControllerOptions(wx.Dialog):

    def __init__(self, *args, **kw):
        super(GlobalControllerOptions, self).__init__(*args, **kw)

        self.cyls = [
            '4',
            '6',
            '8'
        ]

        sizer = wx.BoxSizer(wx.VERTICAL)

        cylSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cylLabel = wx.StaticText(self, wx.ID_ANY, label='Number of Cylinders')
        self.cylCombo = wx.ComboBox(self, wx.ID_ANY, value=self.cyls[0], choices=self.cyls, style=wx.CB_READONLY)
        cylSizer.Add(self.cylLabel, 0, wx.ALL, 5)
        cylSizer.Add(self.cylCombo, 0, wx.ALL, 5)
        sizer.Add(cylSizer, 0, wx.ALL|wx.EXPAND, 5)

        #self.crankLabel = wx.StaticText(self, -1, label='Cranking Advance', pos=(5,45))
        #self.crankSpin = wx.SpinCtrl(self, -1, pos=(colOffset,40), min=0, max=59, initial=0)

        #self.trigLabel = wx.StaticText(self, -1, label='Trigger Offset', pos=(5,75))
        #self.trigSpin = wx.SpinCtrl(self, -1, pos=(colOffset,70), min=0, max=59, initial=0)

        #self.filterLabel = wx.StaticText(self, -1, label='EDIS PIP Filter Level', pos=(5,105))
        #self.filterSpin = wx.SpinCtrl(self, -1, pos=(colOffset,100), min=0, max=1000, initial=0)

        #self.readButton = wx.Button(self, -1, label='Read Options', pos=(100,130))
        #self.writeButton = wx.Button(self, -1, label='Write Options', pos=(200,130))

        #self.okButton = wx.Button(self, -1, label='OK', pos=(200,165))

        self.SetSizer(sizer)
        sizer.Fit(self)
