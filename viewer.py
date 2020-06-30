import numpy as np
import pyglet as pyg
import time

UPDATE_DELAY = 0.5

class Screen(object):
    def __init__(self, dimensions):
        self.width = dimensions[0]
        self.height = dimensions[1]

class Domain(object):
    def __init__(self, dimensions, d0, d1):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.d0 = d0
        self.d1 = d1

    def translate(self, dx, dy):
        x0 = self.d0[0] + dx
        y0 = self.d0[1] + dy
        x1 = x0 + self.width
        y1 = y0 + self.height
        self.d0 = (x0, y0)
        self.d1 = (x1, y1)

class Viewport(object):
    def __init__(self, screen_dimensions = (764, 512), domain_width = 3.0):
        self.screen = Screen(screen_dimensions)

        domain_width = domain_width
        domain_height = domain_width / screen_dimensions[0] * screen_dimensions[1]
        x0 = -domain_width/2.0
        x1 = x0 + domain_width
        y0 = -domain_height/2.0
        y1 = y0 + domain_height
        self.domain = Domain((domain_width, domain_height), (x0, y0), (x1, y1))

        self.x = 0
        self.y = 0

        self.ddx = domain_width / screen_dimensions[0]
        self.ddy = domain_height / screen_dimensions[1]

        self.tupdate = 0.0
        self.__needsUpdate = True

    def needsUpdate(self):
        if self.__needsUpdate and (time.time() > self.tupdate):
            return True
        return False

    def evaluate(self, function):
        v0 = np.empty((self.screen.width, self.screen.height), dtype=np.complex64)
        v1 = np.empty((self.screen.width, self.screen.height), dtype=np.complex64)

        xspan = np.linspace(self.domain.d0[0], self.domain.d1[0], num=self.screen.width, endpoint=True)
        yspan = np.linspace(self.domain.d0[1], self.domain.d1[1], num=self.screen.height, endpoint=True)

        xv, yv = np.meshgrid(xspan, yspan, sparse=False, indexing='xy')

        c = xv + 1j * yv

        fc = function(c)

        self.x = 0
        self.y = 0
        self.__needsUpdate = False

        return fc

    def scroll(self, x, y, dx, dy):
        self.x += dx
        self.y += dy

        self.domain.translate(-dx*self.ddx, -dy*self.ddy)

        self.tupdate = time.time() + UPDATE_DELAY - 0.1
        self.__needsUpdate = True

    def draw(self, image):

        image.blit(self.x, self.y)

        # texture = imageData.get_texture()

        # t = texture.tex_coords
        # print(t)
        # w, h = texture.width, texture.height
        # z = 0.0

        # array = (pyg.gl.GLfloat * 32)(
        #     t[0],           t[1],    t[2],       1.,
        #     self.x,       self.y,       z,       1.,
        #     t[3],           t[4],    t[5],       1.,
        #     self.x + w,   self.y,       z,       1.,
        #     t[6],           t[7],    t[8],       1.,
        #     self.x + w,   self.y + h,   z,       1.,
        #     t[9],          t[10],   t[11],       1.,
        #     self.x,       self.y + h,   z,       1.)

        # pyg.gl.glPushClientAttrib(pyg.gl.GL_CLIENT_VERTEX_ARRAY_BIT)
        # pyg.gl.glInterleavedArrays(pyg.gl.GL_T4F_V4F, 0, array)
        # pyg.gl.glDrawArrays(pyg.gl.GL_QUADS, 0, 4)
        # pyg.gl.glPopClientAttrib()        

viewSize = (764, 512)

view = Viewport(viewSize, 4.0)

def mandelbrot(c):
    z = c
    rv = np.zeros_like(c, dtype=np.int16)

    for _ in range(80):
        z = np.power(z, 2.0) + c
        rv[np.abs(z) < 2.0] += 1

    return rv

def update(dt):
    pass

window = pyg.window.Window()
image = None

@window.event
def on_draw():
    global image

    window.clear()

    if view.needsUpdate():
        values = view.evaluate(mandelbrot)
        imageValues = (255 - (values / 80.0 * 255.0)).astype(np.uint8)
        imageData = imageValues.tobytes()
        image = pyg.image.ImageData(viewSize[0], viewSize[1], 'R', imageData, viewSize[0])
    
    view.draw(image)

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    view.scroll(x, y, scroll_x, scroll_y)
    pyg.clock.schedule_once(update, UPDATE_DELAY)
    
pyg.app.run()
