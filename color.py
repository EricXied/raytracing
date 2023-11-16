from vec3 import Vec3
from interval import Interval
import numpy as np


class Color(Vec3):
    def __init__(self, e=(0, 0, 0)):
        super().__init__(e)

    def write_color(self, samples_per_pixel):
        r = self.x()
        g = self.y()
        b = self.z()

        scale = 1.0 / samples_per_pixel
        r *= scale
        g *= scale
        b *= scale

        r = linear_to_gamma(r)
        g = linear_to_gamma(g)
        b = linear_to_gamma(b)

        interval = Interval(0, 1)

        return Color((interval.clamp(r), interval.clamp(g), (interval.clamp(b))))


def linear_to_gamma(linear):
    return np.sqrt(linear)
