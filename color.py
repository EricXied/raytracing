from vec3 import Vec3
import numpy as np
from interval import Interval


class Color(Vec3):
    def __init__(self, e=(0, 0, 0)):
        super().__init__(e)

    def write_color(self, samples_per_pixel):
        scale = 1.0 / samples_per_pixel
        self.e *= scale
        interval = Interval(0, 1)
        self.e = [interval.clamp(x) for x in self.e]
