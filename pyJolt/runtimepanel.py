import wx
import time
from threading import *
import wx.glcanvas
from OpenGL.GL import *
from OpenGL.GLUT import *

import random

class RuntimePanel(wx.glcanvas.GLCanvas):

    def __init__(self, parent, *args, **kw):
        wx.glcanvas.GLCanvas.__init__(self, parent, *args, **kw)
    
        self.parent = parent

        self.state = None

        self.data = {
            'loadaccel': { #KPa/s
                'data': [1,1,1,1,1,1,1,2,3,4,5],
                'colour': wx.Colour(0, 0, 255),
                'update': self.calculateLoadAccel
            },
            'advance': { #Degrees
                'data': [1,1,1,1,1,1,1,2,3,4,5],
                'colour': wx.Colour(0, 255, 0),
                'update': self.getAdvance
            },
            'rpmaccel': { #RPM/s
                'data': [1,1,1,1,1,1,1,2,3,4,5],
                'colour': wx.Colour(255, 255, 0),
                'update': self.calculateRPMAccel
            },
            'load': { #KPa
                'data': [1,1,1,1,1,1,1,2,3,4,5],
                'colour': wx.Colour(255, 255, 255),
                'update': self.getLoad
            },
            'correction': { #Degrees
                'data': [1,1,1,1,1,1,1,2,3,4,5],
                'colour': wx.Colour(247, 155, 72),
                'update': self.getCorrection
            },
            'rpm': { #RPM
                'data': [1,1,1,1,1,1,1,2,3,4,5],
                'colour': wx.Colour(255, 0, 0),
                'update': self.getRPM
            },
            'aux': { #Water temp?
                'data': [1,1,1,1,1,1,1,2,3,4,5],
                'colour': wx.Colour(255, 0, 255),
                'update': self.getAux
            },
        }

        self.GLInitialized = False

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.onEraseBackground)
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_PAINT, self.onPaint)

        self.Bind(wx.EVT_CLOSE, self.onClose, self)

        self.running = True
        self.timer = Timer(0, self.updateData)        
        self.timer.start()

    def onEraseBackground(self, event):
        pass

    def onSize(self, event):
        context = wx.glcanvas.GLContext(self)
        if context:
            self.parent.Show()
            self.SetCurrent(context)
            size = self.GetClientSize()
            self.OnReshape(size.width, size.height)
            self.Refresh(False)
        event.Skip()
    
    def onPaint(self, event):
        context = wx.glcanvas.GLContext(self)
        if context:
            self.SetCurrent(context)

        if not self.GLInitialized:
            self.OnInitGL()
            self.GLInitialized = True

        self.OnDraw()
        event.Skip()

    def OnInitGL(self):
        glClearColor(1, 1, 1, 1)

    def OnReshape(self, width, height):
        glViewport(0, 0, width, height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-0.5, 0.5, -0.5, 0.5, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def OnDraw(self, *args, **kw):
	glClearColor(0, 0, 0, 1)
       	glClear(GL_COLOR_BUFFER_BIT)

        glBegin(GL_LINES)

        glColor(0.3, 0.3, 0.3)
        for x in range(-10, 10, 1):
            glVertex(x/10.0, -1)
            glVertex(x/10.0, 1)
        for y in range(-10, 10, 1):
            glVertex(-1, y/10.0)
            glVertex(1, y/10.0)
        
        glColor(1, 0, 0)
        for k in self.data.keys():
            data = self.data[k]
            for i in range(0, len(data['data'])-1):
                colour = data['colour']
                glColor(colour.red/255.0, colour.green/255.0, colour.blue/255.0)
                glVertex(-1 + (i/10.0), data['data'][i]/10.0)
                glVertex(-1 + ((i+1)/10.0), data['data'][i+1]/10.0)
        
        glEnd()

        self.SwapBuffers()

    def setState(self, state):
        self.state = state

    def updateData(self):
        while(self.running):
            if self.state:
                for k in self.data.keys():
                    data = self.data[k]
                    newData = data['update']()
                    self.data[k]['data'] = self.rotate(data['data'], newData)

                if bool(self):
                    self.Refresh()
            time.sleep(1)

    def rotate(self, l, newData):
        return l[-1:]+l[:-1]

    def calculateLoadAccel(self):
        return 0 #TODO

    def getAdvance(self):
        return self.state.advance

    def calculateRPMAccel(self):
        return 0 # TODO

    def getLoad(self):
        return self.state.load

    def getCorrection(self):
        return self.state.correctionDegrees

    def getRPM(self):
        return self.state.rpm

    def getAux(self):
        return self.state.aux

    def onClose(self, event):
        self.running = False
        self.Destroy()

