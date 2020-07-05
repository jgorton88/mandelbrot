
import numpy as np
import pyglet as pyg

def RGB(m, MAX_ITERATIONS):
    # normalize to interval [0, 1]
    mnorm = m / MAX_ITERATIONS

    # color mapping
    slope = 1.5
    red   = slope * (mnorm - .5)
    green = 1.0 - slope * np.abs(mnorm - .5)
    blue  = 1.0 - slope * mnorm

    # desaturate a bit
    # desat = 0.2
    # gray = 0.2989*red + 0.5870*green + 0.1140*blue # weights from CCIR 601 spec
    # red = gray * desat + red * (1 - desat)
    # green = gray * desat + green * (1 - desat)
    # blue = gray * desat + blue * (1 - desat)

    red[red < 0.0]     = 0.0
    green[green < 0.0] = 0.0
    blue[blue < 0.0]   = 0.0

    red[m >= MAX_ITERATIONS]   = 0.5
    green[m >= MAX_ITERATIONS] = 0.0
    blue[m >= MAX_ITERATIONS]  = 0.0

    return (255.0 * red, 255.0 * green, 255.0 * blue)

# https://www.codingame.com/playgrounds/2358/how-to-plot-the-mandelbrot-set/adding-some-colors
def rendermono(values, MAX_ITERATIONS): 

    imageValues = (255 - (values / MAX_ITERATIONS * 255.0)).astype(np.uint8)

    imageData = imageValues.tobytes()
    image = pyg.image.ImageData(values.shape[1], values.shape[0], 'R', imageData, values.shape[1])

    return image

def renderstripes(values, MAX_ITERATIONS):
    imageValues = (255.0 * np.fmod(values, 2.0)).astype(np.uint8)

    rgb_values = np.zeros((values.shape[0], values.shape[1]*3))
    rgb_values[:, 0::3] = 0
    rgb_values[:, 1::3] = imageValues
    rgb_values[:, 2::3] = 255 - imageValues

    image_data = rgb_values.astype(np.uint8).tobytes()
    image = pyg.image.ImageData(values.shape[1], values.shape[0], 'RGB', image_data, values.shape[1]*3)

    return image

def render(values, MAX_ITERATIONS):
    red, green, blue = RGB(values, MAX_ITERATIONS)

    rgb_values = np.zeros((values.shape[0], values.shape[1]*3))
    rgb_values[:, 0::3] = red
    rgb_values[:, 1::3] = green
    rgb_values[:, 2::3] = blue

    image_data = rgb_values.astype(np.uint8).tobytes()
    image = pyg.image.ImageData(values.shape[1], values.shape[0], 'RGB', image_data, values.shape[1]*3)

    return image
