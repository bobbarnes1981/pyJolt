import wx
import time
import configurationpanel
import runtimepanel
import tuningpanel
import megajolt
import editrpmloadbins
import configuratoroptions
import globalcontrolleroptions
import loadaxiscalibration
import auxiliaryinputoptions
import aboutpyjolt
from threading import *

class pyJolt(wx.Frame):

    def __init__(self, *args, **kw):
        super(pyJolt, self).__init__(*args, **kw)

        self.state = None

        self.createMenus()

        self.createTools()

        self.CreateStatusBar()

        # TODO: load options?

        self.editBins = editrpmloadbins.EditRpmLoadBins(self)
        self.cOptions = configuratoroptions.ConfiguratorOptions(self)
        self.gcOptions = globalcontrolleroptions.GlobalControllerOptions(self)
        self.laCalibration = loadaxiscalibration.LoadAxisCalibration(self)
        self.auxOptions = auxiliaryinputoptions.AuxiliaryInputOptions(self)
        self.aboutPyJolt = aboutpyjolt.AboutPyJolt(self)

        self.configPanel = configurationpanel.ConfigurationPanel(self)
        self.configPanel.Hide()
        self.runtimePanel = runtimepanel.RuntimePanel(self)
        self.runtimePanel.Hide()
        self.tuningPanel = tuningpanel.TuningPanel(self)
        self.tuningPanel.Hide()

        self.setOptions(self.cOptions.options)
        if self.options.autoRead:
            self.readConfig()

        sizer = wx.BoxSizer()
        sizer.Add(self.configPanel, 1, wx.EXPAND)
        sizer.Add(self.runtimePanel, 1, wx.EXPAND)
        sizer.Add(self.tuningPanel, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.showConfigPanel()

        self.notSaved = False

        self.filepath = None
        self.conf = megajolt.Configuration()
        self.setConfiguration(self.conf)

        self.Bind(wx.EVT_CLOSE, self.onClose, self)

        self.running = True
        self.timer = Timer(0, self.updateState)        
        self.timer.start()

    def updateState(self):
        while(self.running):
            newState = self.coms.getState()
            if self.state and not newState.config == self.state.config:
                self.configSwitched()
            self.state = newState
            self.runtimePanel.setState(self.state)
            time.sleep(1)

    def readConfig(self):
        self.conf = self.coms.getIgnitionConfiguration()
        self.setConfiguration(self.conf)

    def configSwitched(self):
        if not self.options.action == 0:
            if self.options.action == 1:
                #TODO: show confirmation
                return
            # option must be 2 or 1+confirmed
            self.readConfig()

    def showConfigPanel(self):
        self.configPanel.Show()
        self.runtimePanel.Hide()
        self.tuningPanel.Hide()
        self.Layout()
        
    def showRuntimePanel(self):
        self.configPanel.Hide()
        self.runtimePanel.Show()
        self.tuningPanel.Hide()
        self.Layout()

    def showTuningPanel(self):
        self.configPanel.Hide()
        self.runtimePanel.Hide()
        self.tuningPanel.Show()
        self.Layout()

    def updateTitle(self):
        if not self.filepath:
            self.SetTitle('pyJolt - No File Loaded')
        else:
            self.SetTitle('pyJolt - ' + self.filepath)

    def createTools(self):
        emptyBitmap = wx.Bitmap(16, 15, 16)

        toolBar = self.CreateToolBar()

        newConfigItem = toolBar.AddTool(-1, 'New Ignition Configuration', wx.Bitmap('pyJolt/resources/images/tools/new.bmp'), wx.NullBitmap, shortHelp='New Ignition Configuration')
        self.Bind(wx.EVT_TOOL, self.onNewConfig, newConfigItem)

        openConfigItem = toolBar.AddTool(-1, 'Open', wx.Bitmap('pyJolt/resources/images/tools/open.bmp'), wx.NullBitmap, shortHelp='Open')
        self.Bind(wx.EVT_TOOL, self.onOpenConfig, openConfigItem)

        toolBar.AddSeparator()

        saveConfigItem = toolBar.AddTool(-1, 'Save', wx.Bitmap('pyJolt/resources/images/tools/save.bmp'), wx.NullBitmap, shortHelp='Save')
        saveConfigItem.Enable(False)
        self.Bind(wx.EVT_TOOL, self.onSaveConfig, saveConfigItem)

        saveAsConfigItem = toolBar.AddTool(-1, 'Save As', wx.Bitmap('pyJolt/resources/images/tools/saveas.bmp'), wx.NullBitmap,shortHelp='Save As')
        self.Bind(wx.EVT_TOOL, self.onSaveAsConfig, saveAsConfigItem)

        toolBar.AddSeparator()

        getConfigItem = toolBar.AddTool(-1, 'Get Ignition Configuration', wx.Bitmap('pyJolt/resources/images/tools/getconfig.bmp'), wx.NullBitmap, shortHelp='Get Ignition Configuration')
        self.Bind(wx.EVT_TOOL, self.onGetConfig, getConfigItem)

        writeConfigItem = toolBar.AddTool(-1, 'Write Ignition Configuration', wx.Bitmap('pyJolt/resources/images/tools/writeconfig.bmp'), wx.NullBitmap, shortHelp='Write Ignition Configuration')
        self.Bind(wx.EVT_TOOL, self.onWriteConfig, writeConfigItem)

        commitConfigItem = toolBar.AddTool(-1, 'Commit Configuration to Flash', emptyBitmap, wx.NullBitmap, shortHelp='Commit Configuration to Flash')
        self.Bind(wx.EVT_TOOL, self.onCommitConfig, commitConfigItem)

        toolBar.AddSeparator()

        editConfigItem = toolBar.AddTool(-1, 'Edit Ignition Configuration', emptyBitmap, wx.NullBitmap, shortHelp='Edit Ignition Configuration')
        self.Bind(wx.EVT_TOOL, self.onConfigPerspective, editConfigItem)

        runtimeItem = toolBar.AddTool(-1, 'Charting/Runtime View', emptyBitmap, wx.NullBitmap, shortHelp='Charting/Runtime View')
        self.Bind(wx.EVT_TOOL, self.onRuntimePerspective, runtimeItem)

        tuningItem = toolBar.AddTool(-1, 'Tuning', emptyBitmap, wx.NullBitmap, shortHelp='Tuning')
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
        
        saveItem = fileMenu.Append(-1, "Save")
        self.Bind(wx.EVT_MENU, self.onSaveConfig, saveItem)

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
        self.Bind(wx.EVT_MENU, self.onLoadAxisCalibration, axisCalItem)

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
        newConf = megajolt.Configuration()

        self.filepath = None
        self.updateTitle()
        self.conf = newConf
        self.setConfiguration(self.conf)

    def onConfigPerspective(self, menuEvent):
        self.showConfigPanel()

    def onRuntimePerspective(self, menuEvent):
        self.showRuntimePanel()

    def onTuningPerspective(self, menuEvent):
        self.showTuningPanel()

    def onConfiguratorOptions(self, menuEvent):
        if self.cOptions.ShowModal() == wx.ID_OK:
            self.setOptions(self.cOptions.options)

    def onControllerOptions(self, menuEvent):
        self.gcOptions.ShowModal()

    def onLoadAxisCalibration(self, menuEvent):
        self.laCalibration.ShowModal()

    def onAuxInputOptions(self, menuEvent):
        self.auxOptions.ShowModal()

    def onEditBins(self, menuEvent):
        self.editBins.ShowModal()
        #TODO: if OK then update bins from conf?
        #      is it already done through reference?

    def onOpenConfig(self, menuEvent):
        with wx.FileDialog(self, "Open Ignition Configuration", wildcard="MJLJ Configuration Files (*.mjlj)|*.mjlj", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            filepath = fileDialog.GetPath()
        newConf = megajolt.Configuration()
        newConf.load(filepath)

        self.filepath = filepath
        self.updateTitle()
        self.conf = newConf
        self.setConfiguration(self.conf)

    def onSaveConfig(self, menuEvent):
        if self.filepath:
            self.conf.save(self.filepath)

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

            filepath = fileDialog.GetPath()
        self.conf.save(filepath)

        self.filepath = filepath
        self.updateTitle()

    def onExit(self, menuEvent):
        self.Close(True)

    def onAbout(self, menuEvent):
        self.aboutPyJolt.ShowModal()

    def setConfiguration(self, conf):
        self.configPanel.setConfiguration(conf)
        self.editBins.setConfiguration(conf)
        self.tuningPanel.setConfiguration(conf)

    def onClose(self, event):
        if self.notSaved:
            #TODO: confirmation
            return
        self.running = False
        self.tuningPanel.Close()
        self.runtimePanel.Close()
        self.Destroy()

    def setOptions(self, options):
        self.options = options
        self.coms = megajolt.Communication(self.options.comPort)
        self.gcOptions.setCommunication(self.coms)
        #TODO: save?

