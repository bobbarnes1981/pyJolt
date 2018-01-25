import wx
import pyJolt

app = wx.App()

frm = pyJolt.pyJolt(None, title='pyJolt', size=wx.Size(785, 600))

frm.Show()

app.MainLoop()
