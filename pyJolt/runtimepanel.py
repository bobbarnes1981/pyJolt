import wx

class RuntimePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.testData = [
            10, 20, 30, 40, 50, 40, 30, 20, 10
        ]

        self.Bind(wx.EVT_PAINT, self.onPaint)

    def onPaint(self, event):
        dc = wx.PaintDC(self)

        dc.SetBackground(wx.Brush(wx.BLACK))
        dc.Clear()

        dc.SetPen(wx.Pen(wx.RED, 1))

        dc.DrawLine(0,0,30,20)

        dc.SetPen(wx.Pen(wx.BLUE, 1))
        for i in range(0, len(self.testData)-1):
            dc.DrawLine(
                i*10, self.testData[i]*10,
                (i+1)*10, self.testData[i+1]*10)

