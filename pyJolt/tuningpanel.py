import wx
import time
from threading import *
import wx.glcanvas
from OpenGL.GL import *

class TuningPanel(wx.glcanvas.GLCanvas):

    def __init__(self, parent, *args, **kw):
        wx.glcanvas.GLCanvas.__init__(self, parent, *args, **kw)

        self.parent = parent

        self.conf = None

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

        glPushMatrix()

        glRotate(10, 1, 1, 0)
        #glRotate(10, 1, 0, 1)

        glBegin(GL_LINES)

        # base

        glColor(1, 0, 0)

        glVertex(-0.5, -0.5, -0.5) # left - right
        glVertex(0.5, -0.5, -0.5)
        
        glVertex(0.5, -0.5, -0.5) # front - back
        glVertex(0.5, -0.5, 0.5)

        glVertex(0.5, -0.5, 0.5) # right - left
        glVertex(-0.5, -0.5, 0.5)

        glVertex(-0.5, -0.5, 0.5) # back - front
        glVertex(-0.5, -0.5, -0.5)

        # back wall

        glColor(0, 1, 0)

        glVertex(0.5, 0.5, -0.5) # right - left
        glVertex(-0.5, 0.5, -0.5)

        glColor(0.3, 0.3, 0.3)

        glVertex(-0.5, 0.5, -0.5)
        glVertex(-0.5, -0.5, -0.5)

        # right wall

        glColor(0, 0, 1)

        glVertex(0.5, 0.5, -0.5) # front - back
        glVertex(0.5, 0.5, 0.5)

        glColor(0.3, 0.3, 0.3)

        glVertex(0.5, 0.5, -0.5)
        glVertex(0.5, -0.5, -0.5)

        glVertex(0.5, 0.5, 0.5)
        glVertex(0.5, -0.5, 0.5)

        # data

        if self.conf:
            for z in range(0, 9):
                for x in range(0, 9):
                    glVertex(-0.5+((x+1)/10.0), -0.5+((self.conf.advance[z][x]/59.0)), -0.5+((z+1)/10.0))
                    glVertex(-0.5+((x+2)/10.0), -0.5+((self.conf.advance[z][x+1]/59.0)), -0.5+((z+1)/10.0))

        # lines

        glColor(1, 0, 0)
        glVertex(-0.75, 0, 0)
        glVertex(-0.5, 0, 0) #X
        glColor(0, 1, 0)
        glVertex(-0.75, 0, 0)
        glVertex(-0.75, 0.25, 0) #Y
        glColor(0, 0, 1)
        glVertex(-0.75, 0, 0)
        glVertex(-0.75, 0, 0.25) #Z

        glEnd()

        glPopMatrix()

        self.SwapBuffers()

    def updateData(self):
        while(self.running):
            time.sleep(1)

    def setConfiguration(self, conf):
        self.conf = conf
