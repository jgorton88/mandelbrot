import numpy as np
import pyglet as pyg

import time
import math
import threading

from geometry import *
from render import render

UPDATE_DELAY = 0.2

MAX_ITERATIONS = 128

viewSize = (764, 512) # width, height

class Viewport(object):
    def __init__(self, screen_dimensions = (764, 512), function=None, domain_width = 3.0):
        self.function = function

        domain_height = domain_width / screen_dimensions[0] * screen_dimensions[1]
        x0 = -domain_width/2.0
        y0 = -domain_height/2.0
        self.domain = Rect((domain_width, domain_height), (x0, y0))

        self.screen_dim = Point((screen_dimensions[0], screen_dimensions[1]))

        self.view = Rect(self.screen_dim, (0, 0))
        self.scale = 1.0

        self.pitch = Point((self.domain.dim.x / self.screen_dim.x, self.domain.dim.y / self.screen_dim.y))

        self.tupdate = 0.0
        self.__needsUpdate = True

        self.lock = threading.Lock()

    def needsUpdate(self):
        if self.__needsUpdate and (time.time() > self.tupdate):
            return True
        return False

    def evaluate(self):
        xspan = np.linspace(self.domain.p0.x, self.domain.p1.x, num=self.screen_dim.x, endpoint=True)
        yspan = np.linspace(self.domain.p0.y, self.domain.p1.y, num=self.screen_dim.y, endpoint=True)

        xv, yv = np.meshgrid(xspan, yspan, sparse=False, indexing='xy')

        c = xv + 1j * yv

        fc = self.function(c)

        self.view = Rect(self.screen_dim, (0, 0))
        self.scale = 1.0
        self.__needsUpdate = False

        return fc

    def scroll(self, x, y, dx, dy):
        self.lock.acquire()

        self.view += Point((dx, dy))

        self.domain += Point((-dx*self.pitch.x, -dy*self.pitch.y))

        self.tupdate = time.time() + UPDATE_DELAY - 0.05
        self.__needsUpdate = True

        self.lock.release()

    def rescale(self, scale, apply=False):
        self.scale = scale
        self.view = Rect(self.screen_dim, (0, 0)) * scale

        if apply:
            self.domain *= 1.0 / self.scale
            print('domain', self.domain)

            self.pitch = Point((self.domain.dim.x / self.screen_dim.x, self.domain.dim.y / self.screen_dim.y))

            self.tupdate = time.time() + UPDATE_DELAY - 0.05
            self.__needsUpdate = True

    def click(self, x, y):
        self.anchor = Point((x, y))

    def drag(self, x, y, apply=False):
        self.lock.acquire()

        dragged = Point((x, y)) - self.anchor

        ratio = 4.0 * dragged.x / self.screen_dim.x
        dscale = 1.0 + ratio
        bscale = min(max(0.1, dscale), 10.0)

        self.rescale(bscale, apply)

        self.lock.release()
        
def mandelbrot(c):
    z = np.zeros_like(c)
    n = np.zeros_like(c, dtype=np.int16)

    for _ in range(MAX_ITERATIONS):
        z = np.power(z, 2.0) + c
        n[np.abs(z) <= 2.0] += 1

    return n# + 1.0 - np.log2(np.log10(np.abs(z)))

def update(dt):
    pass

window = pyg.window.Window(width=viewSize[0], height=viewSize[1])

@window.event
def on_draw():
    global imageSprite

    window.clear()

    if view.needsUpdate():
        imageSprite = pyg.sprite.Sprite(render(view.evaluate(), MAX_ITERATIONS), x=0, y=0)
    
    if imageSprite != None:
        imageSprite.x = view.view.origin.x
        imageSprite.y = view.view.origin.y
        imageSprite.scale = view.scale
        imageSprite.draw()

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    view.scroll(x, y, scroll_x, scroll_y)
    pyg.clock.schedule_once(update, UPDATE_DELAY)
    
@window.event
def on_mouse_press(x, y, button, modifiers):
    view.click(x, y)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    view.drag(x, y)

@window.event
def on_mouse_release(x, y, button, modifiers):
    view.drag(x, y, apply=True)
    pyg.clock.schedule_once(update, UPDATE_DELAY)

view = Viewport(viewSize, mandelbrot, 4.0)
imageSprite = None
pyg.app.run()
