import wx
import time
from threading import *
import wx.glcanvas
from OpenGL.GL import *
from advancecolours import AdvanceColours

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

        glBegin(GL_LINES)

        minX = -0.4
        maxX = 0.5
        minY = -0.5
        maxY = 0.5
        minZ = -0.8
        maxZ = 1

        # base

        glColor(0.3, 0.3, 0.3)
        glVertex(minX, minY, minZ) # left - right
        glVertex(maxX, minY, minZ)
        glVertex(maxX, minY, minZ) # front - back
        glVertex(maxX, minY, maxZ)
        glVertex(maxX, minY, maxZ) # right - left
        glVertex(minX, minY, maxZ)
        glVertex(minX, minY, maxZ) # back - front
        glVertex(minX, minY, minZ)

        # back wall

        glColor(0.3, 0.3, 0.3)
        glVertex(maxX, maxY, minZ) # right - left
        glVertex(minX, maxY, minZ)

        glColor(0.3, 0.3, 0.3)
        glVertex(minX, maxY, minZ)
        glVertex(minX, minY, minZ)

        # right wall

        glColor(0.3, 0.3, 0.3)
        glVertex(maxX, maxY, minZ) # front - back
        glVertex(maxX, maxY, maxZ)

        glColor(0.3, 0.3, 0.3)
        glVertex(maxX, maxY, minZ)
        glVertex(maxX, minY, minZ)

        glColor(0.3, 0.3, 0.3)
        glVertex(maxX, maxY, maxZ)
        glVertex(maxX, minY, maxZ)

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

        # data

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glBegin(GL_TRIANGLES)
        self.drawVertexes(False)
        glEnd()

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(GL_TRIANGLES)
        self.drawVertexes(True)
        glEnd()

        glPopMatrix()

        self.SwapBuffers()

    def drawVertexes(self, black):
        if self.conf:
            for z in range(0, 9):
                for x in range(0, 9):
                    #left back
                    self.drawVertex(x, z, 0, 0, black)
                    #left front
                    self.drawVertex(x, z, 0, 1, black)
                    #right front
                    self.drawVertex(x, z, 1, 1, black)
                    #right front
                    self.drawVertex(x, z, 1, 1, black)
                    #right back
                    self.drawVertex(x, z, 1, 0, black)
                    #left back
                    self.drawVertex(x, z, 0, 0, black)

    def drawVertex(self, x, z, xo, zo, black):
        if black:
            glColor(0, 0, 0)
        else:
            colour = AdvanceColours.colours[self.conf.advance[z+zo][x+xo]]
            glColor(colour.red/255.0, colour.green/255.0, colour.blue/255.0)
        glVertex(-0.5+((x+1+xo)/10.0), -0.5+((self.conf.advance[z+zo][x+xo]/59.0)), -1+((z+1+zo)/5.0))

    def updateData(self):
        while(self.running):
            time.sleep(1)

    def setConfiguration(self, conf):
        self.conf = conf
