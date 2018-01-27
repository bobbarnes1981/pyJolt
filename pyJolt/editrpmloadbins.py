import wx

class EditRpmLoadBins(wx.Dialog):

    def __init__(self, *args, **kw):
        super(EditRpmLoadBins, self).__init__(*args, **kw)

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizerH = wx.BoxSizer(wx.HORIZONTAL)

        sizerV = wx.BoxSizer(wx.VERTICAL)

        rpmLabel = wx.StaticText(self, wx.ID_ANY, 'RPM Bins')
        loadLabel = wx.StaticText(self, wx.ID_ANY, 'Load Bins')

        sizerV.Add(wx.StaticText(self, wx.ID_ANY), 0, wx.ALL, 5)
        sizerV.Add(rpmLabel, 0, wx.ALL, 5)
        sizerV.Add(loadLabel, 0, wx.ALL, 5)

        sizerH.Add(sizerV, 0, wx.ALL, 5)

        self.rpmBins = []
        self.loadBins = []

        for i in range(0, 10):
            s = wx.BoxSizer(wx.VERTICAL)

            label = wx.StaticText(self, wx.ID_ANY, str(i+1))
            s.Add(label, 0, wx.ALL, 5)

            rpmSpin = wx.SpinCtrl(self, wx.ID_ANY, min=0, max=10000, initial=0, size=(60,-1))
            s.Add(rpmSpin, 0, wx.ALL, 5)
            self.rpmBins.append(rpmSpin)

            loadSpin = wx.SpinCtrl(self, wx.ID_ANY, min=0, max=100, initial=0, size=(60,-1))
            s.Add(loadSpin, 0, wx.ALL, 5)
            self.loadBins.append(loadSpin)

            sizerH.Add(s, 0, wx.ALL, 5)

        sizer.Add(sizerH, 0, wx.ALL, 5)

        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        okButton = wx.Button(self, wx.ID_ANY, 'OK')
        self.Bind(wx.EVT_BUTTON, self.onOkButton, okButton)

        cancelButton = wx.Button(self, wx.ID_ANY, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.onCancelButton, cancelButton)

        buttonSizer.Add(okButton, 0, wx.ALL, 5)
        buttonSizer.Add(cancelButton, 0, wx.ALL, 5)

        sizer.Add(buttonSizer, 0, wx.ALL|wx.ALIGN_CENTRE_HORIZONTAL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def setConfiguration(self, conf):
        self.conf = conf

        for i in range(0, 10):
            self.rpmBins[i].SetValue(self.conf.rpmBins[i]*100)
            self.loadBins[i].SetValue(self.conf.mapBins[i])

    def onOkButton(self, commandEvent):
        for i in range(0, 10):
            self.conf.rpmBins[i] = self.rpmBins[i].GetValue()/100
            self.conf.mapBins[i] = self.loadBins[i].GetValue()
        self.Hide()

    def onCancelButton(self, commandEvent):
        self.setConfiguration(self.conf)
        self.Hide()

