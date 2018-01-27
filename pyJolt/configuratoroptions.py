import wx

class ConfiguratorOptions(wx.Dialog):

    def __init__(self, *args, **kw):
        super(ConfiguratorOptions, self).__init__(*args, **kw)

        self.comPorts = [
            'COM1',
            'COM2'
        ]
        self.actions = [
            'No action',
            'Prompt to read configuration',
            'Auto read configuration'
        ]
        self.loads = [
            'Manifold Absolute Pressure (MAP)',
            'Throttle Position Sensor (TPS)'
        ]

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        comPortSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.comPortLabel = wx.StaticText(self, wx.ID_ANY, label='COM Port')
        self.comPortCombo = wx.ComboBox(self, wx.ID_ANY, value=self.comPorts[0], choices=self.comPorts, style=wx.CB_READONLY)
        comPortSizer.Add(self.comPortLabel, 0, wx.ALL, 5)
        comPortSizer.Add(self.comPortCombo, 0, wx.ALL, 5)
        sizer.Add(comPortSizer, 0, wx.ALL|wx.EXPAND, 5)

        autoReadSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.autoReadCheck = wx.CheckBox(self, wx.ID_ANY, label='Automatically read config at startup')
        autoReadSizer.Add(self.autoReadCheck, 0, wx.ALL, 5)
        sizer.Add(autoReadSizer, 0, wx.ALL|wx.EXPAND, 5)

        actionSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.actionLabel = wx.StaticText(self, wx.ID_ANY, label='When ignition config switched')
        self.actionCombo = wx.ComboBox(self, wx.ID_ANY, value=self.actions[0], choices=self.actions, style=wx.CB_READONLY)
        actionSizer.Add(self.actionLabel, 0, wx.ALL, 5)
        actionSizer.Add(self.actionCombo, 0, wx.ALL, 5)
        sizer.Add(actionSizer, 0, wx.ALL|wx.EXPAND, 5)

        loadSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.loadLabel = wx.StaticText(self, wx.ID_ANY, label='Load Type')
        self.loadCombo = wx.ComboBox(self, wx.ID_ANY, value=self.loads[0], choices=self.loads, style=wx.CB_READONLY)
        loadSizer.Add(self.loadLabel, 0, wx.ALL, 5)
        loadSizer.Add(self.loadCombo, 0, wx.ALL, 5)
        sizer.Add(loadSizer, 0, wx.ALL|wx.EXPAND, 5)

        naSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.naCheck = wx.CheckBox(self, wx.ID_ANY, label='Normally Aspirated Engine')
        naSizer.Add(self.naCheck, 0, wx.ALL, 5)
        sizer.Add(naSizer, 0, wx.ALL|wx.EXPAND, 5)

        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.okButton = wx.Button(self, wx.ID_ANY, label='OK')
        self.cancelButton = wx.Button(self, wx.ID_ANY, label='Cancel')
        buttonSizer.Add(self.okButton, 0, wx.ALL, 5)
        buttonSizer.Add(self.cancelButton, 0, wx.ALL, 5)
        sizer.Add(buttonSizer, 0, wx.ALL|wx.CENTRE, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

