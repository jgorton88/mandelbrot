import numpy as np
import pyglet as pyg

from pyglet.gl import glViewport

import time
import math

from geometry import *
from render import render, renderstripes, rendermono
from screen import Viewport

UPDATE_DELAY = 0.5

MAX_ITERATIONS = 128

VIEW_SIZE = (764, 512) # width, height

def mandelbrot(c):
    z = np.zeros_like(c)

    zesc = np.ones_like(c)
    esc = (np.abs(z) <= 2.0)

    n = np.zeros_like(c, dtype=np.int16)

    for _ in range(MAX_ITERATIONS):
        z = np.power(z, 2.0) + c
        zesc[esc] = z[esc]
        n[np.abs(z) <= 2.0] += 1
        esc = (np.abs(z) <= 2.0)

    # http://linas.org/art-gallery/escape/escape.html
    correction = -np.log(np.log(np.abs(zesc)))/np.log(2.0)
    correction[np.isnan(correction)] = 0.0

    return n + correction

window = pyg.window.Window(width=VIEW_SIZE[0], height=VIEW_SIZE[1], resizable=True)

view = Viewport(VIEW_SIZE, mandelbrot, 4.0, UPDATE_DELAY=UPDATE_DELAY)

imageSprite = None

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

@window.event
def on_resize(width, height):
    global view
    global VIEW_SIZE

    VIEW_SIZE = (width, height)

    glViewport(0, 0, width, height)
    view = Viewport(VIEW_SIZE, mandelbrot, 4.0, tupdate=time.time()+UPDATE_DELAY-0.05,  UPDATE_DELAY=UPDATE_DELAY)
    pyg.clock.schedule_once(update, UPDATE_DELAY)

# dummy update function to help with on_draw event
def update(dt):
    pass

# help with cases when on_resize invokes at startup
pyg.clock.schedule_once(update, 2.0*UPDATE_DELAY)

pyg.app.run()
