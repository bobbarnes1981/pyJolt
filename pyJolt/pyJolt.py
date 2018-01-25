import wx
import configurationpanel
import megajolt

class pyJolt(wx.Frame):

    def __init__(self, *args, **kw):
        super(pyJolt, self).__init__(*args, **kw)

        self.createMenu()

        toolBar = self.CreateToolBar()
        #toolBar.CreateTool()

        self.CreateStatusBar()

        self.configPanel = configurationpanel.ConfigurationPanel(self)

        # TODO: create default config
        conf = megajolt.Configuration()
        self.configPanel.setConfiguration(conf)

    def createMenu(self):
        fileMenu = wx.Menu()
        
        fileMenu.Append(-1, "New")
        
        openItem = fileMenu.Append(-1, "Open")
        self.Bind(wx.EVT_MENU, self.onOpen, openItem)

        fileMenu.AppendSeparator()
        fileMenu.Append(-1, "Save")

        saveAsItem = fileMenu.Append(-1, "Save As")
        self.Bind(wx.EVT_MENU, self.onSaveAs, saveAsItem)
        
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

    def onOpen(self, menuEvent):
        with wx.FileDialog(self, "Open Ignition Configuration", wildcard="MJLJ Configuration Files (*.mjlj)|*.mjlj", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()

    def onSaveAs(self, menuEvent):
        with wx.FileDialog(self, "Save As Ignition Configuration", wildcard="MJLJ Configuration Files (*.mjlj)|*.mjlj", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()

    def onExit(self, menuEvent):
        self.Close(True)

