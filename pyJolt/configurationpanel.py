import wx
import wx.grid
from advancecolours import AdvanceColours

class ConfigurationPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        tabsNb = wx.Notebook(self)

        self.ignitionMap = TabIgnitionMap(tabsNb)
        self.advanceCorrection = TabAdvanceCorrection(tabsNb)
        self.options = TabOptions(tabsNb)

        tabsNb.AddPage(self.ignitionMap, "Ignition Map")
        tabsNb.AddPage(self.advanceCorrection, "Advance Correction")
        tabsNb.AddPage(self.options, "Options")
        
        sizer = wx.BoxSizer()
        sizer.Add(tabsNb, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def setConfiguration(self, conf):
        self.ignitionMap.setConfiguration(conf)
        self.advanceCorrection.setConfiguration(conf)
        self.options.setConfiguration(conf)

class TabIgnitionMap(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        sizerV = wx.BoxSizer(wx.VERTICAL)

        colCellWidth = 50
        colLabelHeight = 30

        rowCellHeight = 20
        rowLabelWidth = 80

        self.colCells = 10
        self.rowCells = 10

        rpmLabel = wx.StaticText(self, label='RPM')
        sizerV.Add(rpmLabel, 0, wx.ALL|wx.ALIGN_CENTRE_HORIZONTAL, 5)

        sizerH = wx.BoxSizer(wx.HORIZONTAL)
        sizerV.Add(sizerH, 0, wx.ALL, 5)

        mapLabel = wx.StaticText(self, label='Load')
        sizerH.Add(mapLabel, 0, wx.ALL|wx.ALIGN_CENTRE_VERTICAL, 5)

        self.grid = wx.grid.Grid(self)
        sizerH.Add(self.grid, 0, wx.ALL, 5)

        self.grid.CreateGrid(self.rowCells, self.colCells)

        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.onGridCellChanged, self.grid)

        cellFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)

        self.grid.SetRowLabelSize(rowLabelWidth)
        for r in range(0, self.rowCells):
            self.grid.SetRowSize(r, rowCellHeight)
        self.grid.SetColLabelSize(colLabelHeight)
        for c in range(0, self.colCells):
            self.grid.SetColSize(c, colCellWidth)
        for r in range(0, self.rowCells):
            for c in range(0, self.colCells):
                self.grid.SetCellFont(r, c, cellFont)
                self.grid.SetCellEditor(r, c, wx.grid.GridCellNumberEditor(0, 59))

        self.SetSizer(sizerV)
            
    def setConfiguration(self, conf):
        self.conf = conf

        for r in range(0, self.rowCells):
            self.grid.SetRowLabelValue(r, str(self.conf.mapBins[r]))

        for c in range(0, self.colCells):
            self.grid.SetColLabelValue(c, str(self.conf.rpmBins[c])+'00')

        for r in range(0, self.rowCells):
            for c in range(0, self.colCells):
                adv = self.conf.advance[r][c]
                self.grid.SetCellValue(r, c, str(adv))
                self.updateGridCellColour(r, c, adv)

    def onGridCellChanged(self, gridEvent):
        adv = int(self.grid.GetCellValue(gridEvent.Row, gridEvent.Col))
        self.updateGridCellColour(gridEvent.Row, gridEvent.Col, adv)
        self.conf.advance[self.rowCells-gridEvent.Row-1][gridEvent.Col] = adv

    def updateGridCellColour(self, row, col, adv):
        self.grid.SetCellBackgroundColour(row, col, AdvanceColours.colours[adv])

class TabAdvanceCorrection(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        colCellWidth = 50
        colLabelHeight = 30

        rowCellHeight = 20
        rowLabelWidth = 80

        self.colCells = 10
        self.rowCells = 2

        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(self.rowCells, self.colCells)
        sizer.Add(self.grid, 0, wx.ALL, 5)

        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.onGridCellChanged, self.grid)

        cellFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)

        self.grid.SetRowLabelSize(rowLabelWidth)
        for r in range(0, self.rowCells):
            if r == 0:
                self.grid.SetRowLabelValue(r, 'Bins')
            if r == 1:
                self.grid.SetRowLabelValue(r, 'Correction')
            self.grid.SetRowSize(r, rowCellHeight)

        self.grid.SetColLabelSize(colLabelHeight)
        for c in range(0, self.colCells):
            self.grid.SetColLabelValue(c, str(c+1))
            self.grid.SetColSize(c, colCellWidth)

        for r in range(0, self.rowCells):
            for c in range(0, self.colCells):
                self.grid.SetCellFont(r, c, cellFont)
                if r == 0:
                    self.grid.SetCellEditor(r, c, wx.grid.GridCellNumberEditor(0, 255))
                if r == 1:
                    self.grid.SetCellEditor(r, c, wx.grid.GridCellNumberEditor(0, 59))

        peakSizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(peakSizer, 0, wx.ALL, 5)

        peakHoldLabel = wx.StaticText(self, wx.ID_ANY, label='Peak Hold For')
        self.peakHoldSpin = wx.SpinCtrl(self, wx.ID_ANY, min=0, max=100, initial=0)
        self.Bind(wx.EVT_SPINCTRL, self.onSpinCtrl, self.peakHoldSpin)
        peakHoldInfoLabel = wx.StaticText(self, wx.ID_ANY, label='Ignition events (0 to disable)')

        peakSizer.Add(peakHoldLabel, 0, wx.ALL, 5)
        peakSizer.Add(self.peakHoldSpin, 0, wx.ALL, 5)
        peakSizer.Add(peakHoldInfoLabel, 0, wx.ALL, 5)

        self.SetSizer(sizer)

    def setConfiguration(self, conf):
        self.conf = conf
        
        for r in range(0, self.rowCells):
            for c in range(0, self.colCells):
                if r == 0:
                    b = self.conf.correctionBins[c]
                    self.grid.SetCellValue(r, c, str(b))
                if r == 1:
                    adv = self.conf.correctionValues[c]
                    self.grid.SetCellValue(r, c, str(adv))
                    self.updateGridCellColour(r, c, adv)

        self.peakHoldSpin.SetValue(self.conf.correctionPeakHold)

    def onGridCellChanged(self, gridEvent):
        val = int(self.grid.GetCellValue(gridEvent.Row, gridEvent.Col))
        if gridEvent.Row == 1:
            self.updateGridCellColour(gridEvent.Row, gridEvent.Col, val)
            self.conf.correctionValues[gridEvent.Col] = val
        if gridEvent.Row == 0:
            self.conf.correctionBins[gridEvent.Col] = val

    def onSpinCtrl(self, spinEvent):
        self.conf.correctionPeakHold = self.peakHoldSpin.GetValue()

    def updateGridCellColour(self, row, col, adv):
        self.grid.SetCellBackgroundColour(row, col, AdvanceColours.colours[adv])

class TabOptions(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.userOutPanel = UserOutsPanel(self)
        self.addOutPanel = AddOutsPanel(self)
        sizer.Add(self.userOutPanel, 0, wx.ALL, 5)
        sizer.Add(self.addOutPanel, 0, wx.ALL, 5)

        self.SetSizer(sizer)

    def setConfiguration(self, conf):
        self.conf = conf

        self.userOutPanel.setConfiguration(self.conf)
        self.addOutPanel.setConfiguration(self.conf)

class UserOutsPanel(wx.Panel):

    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)

        sizer = wx.BoxSizer(wx.VERTICAL)

        userOutLabel = wx.StaticText(self, wx.ID_ANY, label='User Configurable Outputs')
        self.userOuts = [
            UserOutPanel(0, self),
            UserOutPanel(1, self),
            UserOutPanel(2, self),
            UserOutPanel(3, self),
        ]

        sizer.Add(userOutLabel, 0, wx.ALL, 5)
        sizer.Add(self.userOuts[0], 0, wx.ALL, 5)
        sizer.Add(self.userOuts[1], 0, wx.ALL, 5)
        sizer.Add(self.userOuts[2], 0, wx.ALL, 5)
        sizer.Add(self.userOuts[3], 0, wx.ALL, 5)

        self.SetSizer(sizer)

    def setConfiguration(self, conf):
        self.conf = conf

        for i in range(0, 4):
            self.userOuts[i].setConfiguration(self.conf)

class UserOutPanel(wx.Panel):

    def __init__(self, index, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)

        self.index = index

        self.types = [
            'Load',
            'RPM',
            'Aux'
        ]
        self.modes = [
            'Normal',
            'Invert'
        ]

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.label = wx.StaticText(self, wx.ID_ANY, label='Output '+str(index+1))
        sizer.Add(self.label, 0, wx.ALL, 5)

        self.typeCombo = wx.ComboBox(self, wx.ID_ANY, value=self.types[0], choices=self.types, style=wx.CB_READONLY)
        self.Bind(wx.EVT_COMBOBOX, self.onTypeChanged, self.typeCombo)
        sizer.Add(self.typeCombo, 0, wx.ALL, 5)

        self.modeCombo = wx.ComboBox(self, wx.ID_ANY, value=self.modes[0], choices=self.modes, style=wx.CB_READONLY)
        self.Bind(wx.EVT_COMBOBOX, self.onModeChanged, self.modeCombo)
        sizer.Add(self.modeCombo, 0, wx.ALL, 5)

        self.valueSpin = wx.SpinCtrl(self, wx.ID_ANY, min=0, max=10000, initial=0)
        self.Bind(wx.EVT_SPINCTRL, self.onSpinCtrl, self.valueSpin)
        sizer.Add(self.valueSpin, 0, wx.ALL, 5)
    
        self.SetSizer(sizer)

    def setConfiguration(self, conf):
        self.conf = conf

        userOut = self.conf.userOut[self.index]

        self.typeCombo.SetValue(self.types[userOut.type])
        self.modeCombo.SetValue(self.modes[userOut.mode])
        val = userOut.value
        if userOut.type == 1:
            # RPM is displayed as multiples of 100
            val = val * 100
        self.valueSpin.SetValue(val)

    def onTypeChanged(self, commandEvent):
        newTyp = self.types.index(self.typeCombo.GetValue())
        oldTyp = self.conf.userOut[self.index].type
        if newTyp == oldTyp:
            return
        val = self.valueSpin.GetValue()
        if newTyp == 1:
            # changed to RPM multiply by 100
            val = val * 100
        elif oldTyp == 1:
            # changed from RPM divide by 100
            val = val / 100
        self.valueSpin.SetValue(val)
        self.conf.userOut[self.index].type = newTyp

    def onModeChanged(self, commandEvent):
        self.conf.userOut[self.index].mode = self.modes.index(self.modeCombo.GetValue())

    def onSpinCtrl(self, spinEvent):
        t = self.types.index(self.typeCombo.GetValue())
        val = self.valueSpin.GetValue()
        if t == 1:
            # RPM is stored as multiples of 100
            val = val / 100
        self.conf.userOut[self.index].value = val

class AddOutsPanel(wx.Panel):

    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)

        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, wx.ID_ANY, label='Additional Configurable Outputs')
        self.shiftLight = AddOutPanel('shiftLight', 'Shift Light', self)
        self.revLimit = AddOutPanel('revLimit', 'Rev Limit', self)

        sizer.Add(label, 0, wx.ALL, 5)
        sizer.Add(self.shiftLight, 0, wx.ALL, 5)
        sizer.Add(self.revLimit, 0, wx.ALL, 5)

        self.SetSizer(sizer)

    def setConfiguration(self, conf):
        self.conf = conf

        self.shiftLight.setConfiguration(self.conf)
        self.revLimit.setConfiguration(self.conf)

class AddOutPanel(wx.Panel):

    def __init__(self, prop, label, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)

        self.prop = prop

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.label = wx.StaticText(self, wx.ID_ANY, label=label)
        self.valueSpin = wx.SpinCtrl(self, wx.ID_ANY, min=0, max=10000, initial=0)
        self.Bind(wx.EVT_SPINCTRL, self.onSpinCtrl, self.valueSpin)

        sizer.Add(self.label, 0, wx.ALL, 5)
        sizer.Add(self.valueSpin, 0, wx.ALL, 5)

        self.SetSizer(sizer)

    def setConfiguration(self, conf):
        self.conf = conf

        # always represents rpm so multiply by 100
        self.valueSpin.SetValue(getattr(self.conf, self.prop)*100)

    def onSpinCtrl(self, spinEvent):
        # displays as multiple of 100 so lose the last two digits
        setattr(self.conf, self.prop, self.valueSpin.GetValue()/100)

