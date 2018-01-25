import wx
import configurationpanel
import megajolt

class pyJolt(wx.Frame):

    def __init__(self, *args, **kw):
        super(pyJolt, self).__init__(*args, **kw)

        self.createMenus()

        self.createTools()

        self.CreateStatusBar()

        self.configPanel = configurationpanel.ConfigurationPanel(self)

        # TODO: create default config
        conf = megajolt.Configuration()
        self.configPanel.setConfiguration(conf)

    def createTools(self):
        emptyBitmap = wx.EmptyBitmap(16, 15, 16)
        #wx.Bitmap('')

        toolBar = self.CreateToolBar()

        newConfigItem = toolBar.AddLabelTool(-1, 'New Ignition Configuration', emptyBitmap, wx.NullBitmap)
        self.Bind(wx.EVT_TOOL, self.onNewConfig, newConfigItem)

        openConfigItem = toolBar.AddLabelTool(-1, 'Open', emptyBitmap, wx.NullBitmap)
        self.Bind(wx.EVT_TOOL, self.onOpenConfig, openConfigItem)

        toolBar.AddSeparator()

        saveConfigItem = toolBar.AddLabelTool(-1, 'Save', emptyBitmap, wx.NullBitmap)
        saveConfigItem.Enable(False)
        self.Bind(wx.EVT_TOOL, self.onSaveConfig, saveConfigItem)

        saveAsConfigItem = toolBar.AddLabelTool(-1, 'Save As', emptyBitmap, wx.NullBitmap)
        self.Bind(wx.EVT_TOOL, self.onSaveAsConfig, saveAsConfigItem)

        toolBar.AddSeparator()

        getConfigItem = toolBar.AddLabelTool(-1, 'Get Ignition Configuration', emptyBitmap, wx.NullBitmap)
        self.Bind(wx.EVT_TOOL, self.onGetConfig, getConfigItem)

        writeConfigItem = toolBar.AddLabelTool(-1, 'Write Ignition Configuration', emptyBitmap, wx.NullBitmap)
        self.Bind(wx.EVT_TOOL, self.onWriteConfig, writeConfigItem)

        commitConfigItem = toolBar.AddLabelTool(-1, 'Commit Configuration to Flash', emptyBitmap, wx.NullBitmap)
        self.Bind(wx.EVT_TOOL, self.onCommitConfig, commitConfigItem)

        toolBar.AddSeparator()

        editConfigItem = toolBar.AddLabelTool(-1, 'Edit Ignition Configuration', emptyBitmap, wx.NullBitmap)
        self.Bind(wx.EVT_TOOL, self.onConfigPerspective, editConfigItem)

        runtimeItem = toolBar.AddLabelTool(-1, 'Charting/Runtime View', emptyBitmap, wx.NullBitmap)
        self.Bind(wx.EVT_TOOL, self.onRuntimePerspective, runtimeItem)

        tuningItem = toolBar.AddLabelTool(-1, 'Tuning', emptyBitmap, wx.NullBitmap)
        self.Bind(wx.EVT_TOOL, self.onTuningPerspective, tuningItem)

    def createMenus(self):
        fileMenu = self.createFileMenu()
        editMenu = self.createEditMenu()
        toolsMenu = self.createToolsMenu()
        viewMenu = wx.Menu()
        perspectiveMenu = self.createPerspectiveMenu()
        helpMenu = self.createHelpMenu()

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "File")
        menuBar.Append(editMenu, "Edit")
        menuBar.Append(toolsMenu, "Tools")
        menuBar.Append(viewMenu, "View")
        menuBar.Append(perspectiveMenu, "Perspective")
        menuBar.Append(helpMenu, "Help")

        self.SetMenuBar(menuBar)

    def createFileMenu(self):
        fileMenu = wx.Menu()
        
        newConfigItem = fileMenu.Append(-1, "New")
        self.Bind(wx.EVT_MENU, self.onNewConfig, newConfigItem)
        
        openItem = fileMenu.Append(-1, "Open")
        self.Bind(wx.EVT_MENU, self.onOpenConfig, openItem)

        fileMenu.AppendSeparator()
        fileMenu.Append(-1, "Save")

        saveAsItem = fileMenu.Append(-1, "Save As")
        self.Bind(wx.EVT_MENU, self.onSaveAsConfig, saveAsItem)
        
        fileMenu.AppendSeparator()
        fileMenu.Append(-1, "Quick Datalog")
        fileMenu.Append(-1, "Start Datalog")
        fileMenu.Append(-1, "Mark Datalog")
        stopDatalogItem = fileMenu.Append(-1, "Stop Datalog")
        stopDatalogItem.Enable(False)
        fileMenu.Append(-1, "Open Datalog")
        fileMenu.AppendSeparator()

        exitItem = fileMenu.Append(wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.onExit, exitItem)

        return fileMenu

    def createEditMenu(self):
        editMenu = wx.Menu()

        editBinsItem = editMenu.Append(-1, "Edit RPM and Load Bins")
        self.Bind(wx.EVT_MENU, self.onEditBins, editBinsItem)

        return editMenu

    def createToolsMenu(self):
        toolsMenu = wx.Menu()

        configuratorItem = toolsMenu.Append(-1, "Configurator Options")
        self.Bind(wx.EVT_MENU, self.onConfiguratorOptions, configuratorItem)

        controllerItem = toolsMenu.Append(-1, "Global Controller Options")
        self.Bind(wx.EVT_MENU, self.onControllerOptions, controllerItem)

        axisCalItem = toolsMenu.Append(-1, "Load Axis Calibration")
        self.Bind(wx.EVT_MENU, self.onAxisCalibration, axisCalItem)

        auxInputItem = toolsMenu.Append(-1, "Auxiliary Input Options")
        self.Bind(wx.EVT_MENU, self.onAuxInputOptions, auxInputItem)

        return toolsMenu

    def createPerspectiveMenu(self):
        perspectiveMenu = wx.Menu()

        configItem = perspectiveMenu.Append(-1, "Configuration")
        self.Bind(wx.EVT_MENU, self.onConfigPerspective, configItem)

        runtimeItem = perspectiveMenu.Append(-1, "Runtime")
        self.Bind(wx.EVT_MENU, self.onRuntimePerspective, runtimeItem)

        tuningItem = perspectiveMenu.Append(-1, "Tuning")
        self.Bind(wx.EVT_MENU, self.onTuningPerspective, tuningItem)

        return perspectiveMenu

    def createHelpMenu(self):
        helpMenu = wx.Menu()

        helpItem = helpMenu.Append(-1, "About pyJolt")
        self.Bind(wx.EVT_MENU, self.onAbout, helpItem)

        return helpMenu

    def onNewConfig(self, menuEvent):
        pass

    def onConfigPerspective(self, menuEvent):
        pass

    def onRuntimePerspective(self, menuEvent):
        pass

    def onTuningPerspective(self, menuEvent):
        pass

    def onConfiguratorOptions(self, menuEvent):
        pass

    def onControllerOptions(self, menuEvent):
        pass

    def onAxisCalibration(self, menuEvent):
        pass

    def onAuxInputOptions(self, menuEvent):
        pass

    def onEditBins(self, menuEvent):
        pass

    def onOpenConfig(self, menuEvent):
        with wx.FileDialog(self, "Open Ignition Configuration", wildcard="MJLJ Configuration Files (*.mjlj)|*.mjlj", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()

    def onSaveConfig(self, menuEvent):
        pass

    def onGetConfig(self, menuEvent):
        pass

    def onWriteConfig(self, menuEvent):
        pass

    def onCommitConfig(self, menuEvent):
        pass

    def onSaveAsConfig(self, menuEvent):
        with wx.FileDialog(self, "Save As Ignition Configuration", wildcard="MJLJ Configuration Files (*.mjlj)|*.mjlj", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()

    def onExit(self, menuEvent):
        self.Close(True)

    def onAbout(self, menuEvent):
        pass
