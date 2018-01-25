import wx
import wx.grid

import configuration

class AdvanceColours():

    colours = [
        wx.Colour(111,  0,255), # 0
        wx.Colour(132,  0,255), # 1
        wx.Colour(153,  0,255), # 2
        wx.Colour(174,  0,255), # 3
        wx.Colour(195,  0,255), # 4
        wx.Colour(217,  0,255), # 5
        wx.Colour(238,  0,255), # 6
        wx.Colour(255,  0,255), # 7
        wx.Colour(255,  0,251), # 8
        wx.Colour(255,  0,230), # 9

        wx.Colour(255,  0,208), #10
        wx.Colour(255,  0,187), #11
        wx.Colour(255,  0,166), #12
        wx.Colour(255,  0,144), #13
        wx.Colour(255,  0,123), #14
        wx.Colour(255,  0,102), #15
        wx.Colour(255,  0, 81), #16
        wx.Colour(255,  0, 59), #17
        wx.Colour(255,  0, 38), #18
        wx.Colour(255,  0, 17), #19

        wx.Colour(255, 30,  0), #20
        wx.Colour(255, 51,  0), #21
        wx.Colour(255, 72,  0), #22
        wx.Colour(255, 93,  0), #23
        wx.Colour(255,115,  0), #24
        wx.Colour(255,136,  0), #25
        wx.Colour(255,157,  0), #26
        wx.Colour(255,178,  0), #27
        wx.Colour(255,200,  0), #28
        wx.Colour(255,221,  0), #29

        wx.Colour(255,242,  0), #30
        wx.Colour(255,255,  0), #31
        wx.Colour(255,255,  0), #32
        wx.Colour(255,255,  0), #33
        wx.Colour(255,255, 22), #34
        wx.Colour(255,255, 33), #35
        wx.Colour(255,255, 44), #36
        wx.Colour(255,255, 55), #37
        wx.Colour(255,255, 66), #38
        wx.Colour(255,255, 77), #39

        wx.Colour(255,255, 88), #40
        wx.Colour(255,255, 99), #41
        wx.Colour(255,255,110), #42
        wx.Colour(255,255,121), #43
        wx.Colour(255,255,132), #44
        wx.Colour(255,255,143), #45
        wx.Colour(255,255,154), #46
        wx.Colour(255,255,165), #47
        wx.Colour(255,255,176), #48
        wx.Colour(255,255,187), #49

        wx.Colour(255,255,198), #50
        wx.Colour(255,255,209), #51
        wx.Colour(255,255,220), #52
        wx.Colour(255,255,231), #53
        wx.Colour(255,255,242), #54
        wx.Colour(255,255,253), #55
        wx.Colour(255,255,255), #56
        wx.Colour(255,255,255), #57
        wx.Colour(255,255,255), #58
        wx.Colour(255,255,255), #59
    ]

class TabIgnitionMap(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.colCellWidth = 50
        self.colLabelHeight = 30

        self.rowCellHeight = 20
        self.rowLabelWidth = 80

        self.rpmLabelOffset = 10
        self.mapLabelOffset = 10

    def setConfiguration(self, conf):
        self.conf = conf

        colCells = len(self.conf.rpmBins)

        rowCells = len(self.conf.mapBins)

        width = (colCells*self.colCellWidth)+self.rowLabelWidth
        height = (rowCells*self.rowCellHeight)+self.colLabelHeight

        rpmLabel = wx.StaticText(self, label='RPM', pos=(width/2,self.rpmLabelOffset))
        mapLabel = wx.StaticText(self, label='Load', pos=(self.mapLabelOffset,((self.rpmLabelOffset+height)/2)+rpmLabel.Size.height))

        gridXOffset = 20 + self.mapLabelOffset + mapLabel.Size.width
        gridYOffset = 20 + self.rpmLabelOffset + rpmLabel.Size.height

        self.grid = wx.grid.Grid(self, pos=(gridXOffset,gridYOffset), size=(width,height))
        self.grid.CreateGrid(rowCells, colCells)

        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.onGridCellChanged, self.grid)

        cellFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True)

        self.grid.SetRowLabelSize(self.rowLabelWidth)
        for r in range(0, rowCells):
            self.grid.SetRowLabelValue(r, str(self.conf.mapBins[r]))
            self.grid.SetRowSize(r, self.rowCellHeight)

        self.grid.SetColLabelSize(self.colLabelHeight)
        for c in range(0, colCells):
            self.grid.SetColLabelValue(c, str(self.conf.rpmBins[c]) + '00')
            self.grid.SetColSize(c, self.colCellWidth)

        for r in range(0, rowCells):
            for c in range(0, colCells):
                self.grid.SetCellFont(r, c, cellFont)
                self.grid.SetCellEditor(r, c, wx.grid.GridCellNumberEditor(0, 59))
                adv = self.conf.advance[rowCells-r-1][c]
                self.grid.SetCellValue(r, c, str(adv))
                self.updateGridCellColour(r, c, adv)

    def onGridCellChanged(self, gridEvent):
        adv = int(self.grid.GetCellValue(gridEvent.Row, gridEvent.Col))
        self.updateGridCellColour(gridEvent.Row, gridEvent.Col, adv)

    def updateGridCellColour(self, row, col, adv):
        self.grid.SetCellBackgroundColour(row, col, AdvanceColours.colours[adv])
        

class TabAdvanceCorrection(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.colCellWidth = 50
        self.colLabelHeight = 30

        self.rowCellHeight = 20
        self.rowLabelWidth = 80

    def setConfiguration(self, conf):
        self.conf = conf
        
        colCells = len(self.conf.correctionBins)

        rowCells = 2

        width = (colCells*self.colCellWidth)+self.rowLabelWidth
        height = (rowCells*self.rowCellHeight)+self.colLabelHeight

        gridXOffset = 20
        gridYOffset = 20

        self.grid = wx.grid.Grid(self, pos=(gridXOffset,gridYOffset), size=(width,height))
        self.grid.CreateGrid(rowCells, colCells)

        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.onGridCellChanged, self.grid)

        cellFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True)

        self.grid.SetRowLabelSize(self.rowLabelWidth)
        for r in range(0, rowCells):
            if r == 0:
                self.grid.SetRowLabelValue(r, 'Bins')
            if r == 1:
                self.grid.SetRowLabelValue(r, 'Correction')
            self.grid.SetRowSize(r, self.rowCellHeight)

        self.grid.SetColLabelSize(self.colLabelHeight)
        for c in range(0, colCells):
            self.grid.SetColLabelValue(c, str(c+1))
            self.grid.SetColSize(c, self.colCellWidth)

        for r in range(0, rowCells):
            for c in range(0, colCells):
                self.grid.SetCellFont(r, c, cellFont)
                if r == 0:
                    self.grid.SetCellEditor(r, c, wx.grid.GridCellNumberEditor(0, 255))
                    b = self.conf.correctionBins[c]
                    self.grid.SetCellValue(r, c, str(b))

                if r == 1:
                    self.grid.SetCellEditor(r, c, wx.grid.GridCellNumberEditor(0, 59))
                    adv = self.conf.correctionValues[c]
                    self.grid.SetCellValue(r, c, str(adv))
                    self.updateGridCellColour(r, c, adv)

        options = wx.Panel(self, pos=(20, gridYOffset+self.grid.Size.height+20),size=(width,height))
        peakHoldLabel = wx.StaticText(options, -1, label='Peak Hold For', pos=(0, 0))

    def onGridCellChanged(self, gridEvent):
        if gridEvent.Row == 1:
            adv = int(self.grid.GetCellValue(gridEvent.Row, gridEvent.Col))
            self.updateGridCellColour(gridEvent.Row, gridEvent.Col, adv)

    def updateGridCellColour(self, row, col, adv):
        self.grid.SetCellBackgroundColour(row, col, AdvanceColours.colours[adv])

class TabOptions(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

    def setConfiguration(self, conf):
        self.conf = conf

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

class pyJolt(wx.Frame):

    def __init__(self, *args, **kw):
        super(pyJolt, self).__init__(*args, **kw)
        
        fileMenu = wx.Menu()
        fileMenu.Append(-1, "New")
        fileMenu.Append(-1, "Open")
        fileMenu.AppendSeparator()
        #save
        #saveas
        #---
        #DATALOG STUFF
        #---
        fileMenu.Append(wx.ID_EXIT)

        editMenu = wx.Menu()
        toolsMenu = wx.Menu()
        viewMenu = wx.Menu()
        perspectiveMenu = wx.Menu()
        helpMenu = wx.Menu()

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "File")
        menuBar.Append(editMenu, "Edit")
        menuBar.Append(toolsMenu, "Tools")
        menuBar.Append(viewMenu, "View")
        menuBar.Append(perspectiveMenu, "Perspective")
        menuBar.Append(helpMenu, "Help")

        self.SetMenuBar(menuBar)

        toolBar = self.CreateToolBar()
        #toolBar.CreateTool()

        self.CreateStatusBar()

        self.configPanel = ConfigurationPanel(self)

        # TODO: create default config
        conf = configuration.Configuration()
        self.configPanel.setConfiguration(conf)

