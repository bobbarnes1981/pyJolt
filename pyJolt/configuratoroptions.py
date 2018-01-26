import wx

class ConfiguratorOptions(wx.Dialog):

    def __init__(self, *args, **kw):
        super(ConfiguratorOptions, self).__init__(*args, **kw)

        colOffset = 205

        self.comPorts = [
            'COM1',
            'COM2'
        ]

        self.comPortLabel = wx.StaticText(self, -1, label='COM Port', pos=(5,10))
        self.comPortCombo = wx.ComboBox(self, -1, value=self.comPorts[0], pos=(colOffset,5), choices=self.comPorts, style=wx.CB_READONLY)

        self.autoReadCheck = wx.CheckBox(self, -1, label='Automatically read config at startup', pos=(colOffset, 35))

        self.actions = [
            'No action',
            'Prompt to read configuration',
            'Auto read configuration'
        ]
    
        self.actionLabel = wx.StaticText(self, -1, label='When ignition config switched', pos=(5, 70))
        self.actionCombo = wx.ComboBox(self, -1, value=self.actions[0], pos=(colOffset,65), choices=self.actions, style=wx.CB_READONLY)

        self.loads = [
            'Manifold Absolute Pressure (MAP)',
            'Throttle Position Sensor (TPS)'
        ]

        self.loadLabel = wx.StaticText(self, -1, label='Load Type', pos=(5,100))
        self.loadCombo = wx.ComboBox(self, -1, value=self.loads[0], pos=(colOffset,95), choices=self.loads, style=wx.CB_READONLY)

        self.naCheck = wx.CheckBox(self, -1, label='Normally Aspirated Engine', pos=(colOffset,125))

        self.okButton = wx.Button(self, -1, label='OK', pos=(300, 155))
        self.cancelButton = wx.Button(self, -1, label='Cancel', pos=(400,155))

