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

        crankSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.crankLabel = wx.StaticText(self, wx.ID_ANY, label='Cranking Advance')
        self.crankSpin = wx.SpinCtrl(self, wx.ID_ANY, min=0, max=59, initial=0)
        crankSizer.Add(self.crankLabel, 0, wx.ALL, 5)
        crankSizer.Add(self.crankSpin, 0, wx.ALL, 5)
        sizer.Add(crankSizer, 0, wx.ALL|wx.EXPAND, 5)

        trigSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.trigLabel = wx.StaticText(self, wx.ID_ANY, label='Trigger Offset')
        self.trigSpin = wx.SpinCtrl(self, wx.ID_ANY, min=0, max=59, initial=0)
        trigSizer.Add(self.trigLabel, 0, wx.ALL, 5)
        trigSizer.Add(self.trigSpin, 0, wx.ALL, 5)
        sizer.Add(trigSizer, 0, wx.ALL|wx.EXPAND, 5)

        filterSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.filterLabel = wx.StaticText(self, wx.ID_ANY, label='EDIS PIP Filter Level')
        self.filterSpin = wx.SpinCtrl(self, wx.ID_ANY, min=0, max=1000, initial=0)
        filterSizer.Add(self.filterLabel, 0, wx.ALL, 5)
        filterSizer.Add(self.filterSpin, 0, wx.ALL, 5)
        sizer.Add(filterSizer, 0, wx.ALL|wx.EXPAND, 5)

        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.readButton = wx.Button(self, wx.ID_ANY, label='Read Options')
        self.Bind(wx.EVT_BUTTON, self.onReadButton, self.readButton)
        self.writeButton = wx.Button(self, wx.ID_ANY, label='Write Options')
        self.Bind(wx.EVT_BUTTON, self.onWriteButton, self.writeButton)
        buttonSizer.Add(self.readButton, 0, wx.ALL, 5)
        buttonSizer.Add(self.writeButton, 0, wx.ALL, 5)
        sizer.Add(buttonSizer, 0, wx.ALL|wx.CENTRE, 5)

        okSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.okButton = wx.Button(self, wx.ID_ANY, label='OK')
        self.Bind(wx.EVT_BUTTON, self.onOkButton, self.okButton)
        okSizer.Add(self.okButton, 0, wx.ALL, 5)
        sizer.Add(okSizer, 0, wx.ALL|wx.CENTRE, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def setCommunication(self, coms):
        self.coms = coms

    def setOptions(self, options):
        #TODO: use real values
        self.coms.updateGlobalConfiguration(0, 0, 0, 0)

    def onReadButton(self, commandEvent):
        #TODO: update UI
        self.coms.getGlobalConfiguration()

    def onWriteButton(self, commandEvent):
        pass

    def onOkButton(self, commandEvent):
        self.Hide()
