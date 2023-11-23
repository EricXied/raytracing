from external.rtw_image import RtwImage
from color import Color
from interval import Interval
from perlin import Perlin
import numpy as np


class Texture:
    def __init__(self):
        pass

    def color(self, u, v, p):
        pass


class SolidColor:
    def __init__(self, c):
        self.color_value = c

    def value(self, u, v, p):
        return self.color_value


class CheckerTexture:
    def __init__(self, scale, even, odd):
        self.inv_scale = scale
        self.even = SolidColor(even)
        self.odd = SolidColor(odd)

    def value(self, u, v, p):
        xinteger = int(self.inv_scale * p.x())
        yinteger = int(self.inv_scale * p.y())
        zinteger = int(self.inv_scale * p.z())
        is_even = (xinteger + yinteger + zinteger) % 2 == 0
        return self.even.value(u, v, p) if is_even else self.odd.value(u, v, p)


class ImageTexture:

    def __init__(self, filename):
        self.image = RtwImage(filename)

    def value(self, u, v, p):
        if not self.image.height():
            return Color((0, 1, 1))
        u = Interval(0, 1).clamp(u)
        v = 1.0 - Interval(0, 1).clamp(v)

        i = u * self.image.width()
        j = v * self.image.height()
        pixel = self.image.pixel_data(i, j)

        color_scale = 1.0 / 255.0
        return Color((pixel[0] * color_scale, pixel[1] * color_scale, pixel[2] * color_scale))


class NoiseTexture:
    def __init__(self, sc):
        self.noise = Perlin()
        self.sc = sc

    def value(self, u, v, p):
        s = self.sc * p
        # marbled texture
        return Color((1, 1, 1)) * 0.5 * (1 + np.sin(s.z() + 10 * self.noise.turb(s)))
        # turbulence
        # return Color((1, 1, 1)) * self.noise.turb(s)
        # smoothed perlin
        # return Color((1, 1, 1)) * 0.5 * (1 + self.noise.noise(p * self.sc))
