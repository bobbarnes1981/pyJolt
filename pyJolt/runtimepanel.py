import wx
import time
from threading import *
from wx.lib import plot

import random

class RuntimePanel(plot.PlotCanvas):

    def __init__(self, *args, **kw):
        plot.PlotCanvas.__init__(self, *args, **kw)

        self.SetBackgroundColour(wx.BLACK)

        self.x_data = [1,2,3,4,5,6,7,8,9,10]

        self.y1_data = [1,2,3,4,5,6,7,8,9,10]
        self.y2_data = [8,7,6,5,4,5,6,7,8,9]

        self.running = True

        self.timer = Timer(0, self.updateData)
        self.timer.start()

    def updateData(self):
        count = 0
        while(self.running):
            count += 1

            print('update: '+ str(count))
        
            xy1_data = list(zip(self.x_data, self.y1_data))
            xy2_data = list(zip(self.x_data, self.y2_data))

            line1 = plot.PolySpline(
                xy1_data,
                colour=wx.RED,
                width=2
            )
            line2 = plot.PolySpline(
                xy2_data,
                colour=wx.BLUE,
                width=2
            )
            graphics = plot.PlotGraphics([line1,line2])
            axes_pen = wx.Pen(wx.WHITE, 1, wx.PENSTYLE_LONG_DASH)
            self.axesPen = axes_pen
            self.Draw(graphics)

            self.y1_data = self.rotate(self.y1_data)
            self.y2_data = self.rotate(self.y2_data)

            #self.testData[self.testDataMax-1] = random.randint(0, 255)
            
            time.sleep(1)

    def rotate(self, l):
        return l[-1:]+l[:-1]
