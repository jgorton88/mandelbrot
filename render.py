
import numpy as np
import pyglet as pyg

from PIL import Image

def HSV(m, MAX_ITERATIONS):
    hue = (255.0 * (m / MAX_ITERATIONS))
    saturation = 255.0 * np.ones_like(m)
    value = 255.0 * np.ones_like(m)
    value[m >= MAX_ITERATIONS] = 0.0

    return (hue, saturation, value)

def RGB(m, MAX_ITERATIONS):
    mnorm = m / MAX_ITERATIONS # 0 .. 1

    red   = 2.0 * (mnorm - .5)
    green = 1.0 - 2.0 * np.abs(mnorm - .5)
    blue  = 1.0 - 2.0 * mnorm

    red[red < 0.0]     = 0.0
    green[green < 0.0] = 0.0
    blue[blue < 0.0]   = 0.0

    red[m >= MAX_ITERATIONS]   = 0.0
    green[m >= MAX_ITERATIONS] = 0.0
    blue[m >= MAX_ITERATIONS]  = 0.0

    return (255.0 * red, 255.0 * green, 255.0 * blue)

# https://www.codingame.com/playgrounds/2358/how-to-plot-the-mandelbrot-set/adding-some-colors
def rendermono(values, MAX_ITERATIONS): 

    imageValues = (255 - (values / MAX_ITERATIONS * 255.0)).astype(np.uint8)

    imageData = imageValues.tobytes()
    image = pyg.image.ImageData(values.shape[1], values.shape[0], 'R', imageData, values.shape[1])

    return image

# def render(values, MAX_ITERATIONS):
#     hues, saturations, values = HSV(values, MAX_ITERATIONS)
#     hsv_values = np.zeros((values.shape[0], values.shape[1]*3))
#     hsv_values[:, 0::3] = hues
#     hsv_values[:, 1::3] = saturations
#     hsv_values[:, 2::3] = values
#     image_data = Image.frombytes('HSV', values.shape, hsv_values.astype(np.uint8).tobytes()).convert('RGB').tobytes()
#     image = pyg.image.ImageData(values.shape[1], values.shape[0], 'RGB', image_data, values.shape[1]*3)
#     return image

def render(values, MAX_ITERATIONS):
    red, green, blue = RGB(values, MAX_ITERATIONS)

    rgb_values = np.zeros((values.shape[0], values.shape[1]*3))
    rgb_values[:, 0::3] = red
    rgb_values[:, 1::3] = green
    rgb_values[:, 2::3] = blue

    image_data = rgb_values.astype(np.uint8).tobytes()
    image = pyg.image.ImageData(values.shape[1], values.shape[0], 'RGB', image_data, values.shape[1]*3)

    return image
