import wx

class AboutPyJolt(wx.Dialog):

    def __init__(self, *args, **kw):
        super(AboutPyJolt, self).__init__(*args, **kw)

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        label = wx.StaticText(self, label='pyJolt')
        sizer.Add(label, 0, wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
