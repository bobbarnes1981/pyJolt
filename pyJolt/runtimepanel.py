import wx
import time
from threading import *
import wx.glcanvas
from OpenGL.GL import *

import random

class RuntimePanel(wx.glcanvas.GLCanvas):

    def __init__(self, parent, *args, **kw):
        wx.glcanvas.GLCanvas.__init__(self, parent, *args, **kw)
    
        self.parent = parent

        self.data = {
            'rpm': [1,1,1,1,1,1,1,2,3,4,5]
        }

        self.GLInitialized = False

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.onEraseBackground)
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_PAINT, self.onPaint)

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
            self.onReshape(size.width, size.height)
            self.Refresh(False)
        event.Skip()
    
    def onPaint(self, event):
        context = wx.glcanvas.GLContext(self)
        if context:
            self.SetCurrent(context)

        if not self.GLInitialized:
            self.onInitGL()
            self.GLInitialized = True

        self.onDraw()
        event.Skip()

    def onInitGL(self):
        glClearColor(1, 1, 1, 1)

    def onReshape(self, width, height):
        glViewport(0, 0, width, height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-0.5, 0.5, -0.5, 0.5, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def onDraw(self, *args, **kw):
	glClearColor(0, 0, 0, 1)
       	glClear(GL_COLOR_BUFFER_BIT)

        glBegin(GL_LINES)
        glColor(0.3, 0.3, 0.3)
        for x in [-1, -0.5, 0, 0.5, 1]:
            glVertex(x, -1)
            glVertex(x, 1)
        for y in [-1, -0.5, 0, 0.5, 1]:
            glVertex(-1, y)
            glVertex(1, y)
        glEnd()

        # Drawing an example triangle in the middle of the screen
        glBegin(GL_TRIANGLES)
        glColor(1, 0, 0)
        glVertex(-.25, -.25)
        glVertex(.25, -.25)
        glVertex(0, .25)
        glEnd()

        self.SwapBuffers()

    def updateData(self):
        while(self.running):

            for k in self.data.keys():
                self.data[k] = self.rotate(self.data[k])

            self.onDraw()

            time.sleep(1)

    def rotate(self, l):
        return l[-1:]+l[:-1]

