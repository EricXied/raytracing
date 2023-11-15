from vec3 import Vec3
import numpy as np

image_width = 256
image_height = 256


class Color(Vec3):
    def __init__(self, e):
        super().__init__(e)
        self.e = np.array(e)
