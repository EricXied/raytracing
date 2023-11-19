import numpy as np
from utilities import random_double


class Vec3:
    def __init__(self, e=(0, 0, 0)):
        try:
            self.e = np.array(e.e)
        except:
            self.e = np.array(e)

    def __repr__(self):
        return f'Vector:{self.e}'

    def x(self):
        return self.e[0]

    def y(self):
        return self.e[1]

    def z(self):
        return self.e[2]

    def __add__(self, other):

        return Vec3(self.e + other.e)

    def __sub__(self, other):
        return Vec3(self.e - other.e)

    def __mul__(self, t):
        try:
            return Vec3(np.array(self.e) * np.array(t.e))
        except:
            return Vec3(np.array(self.e) * t)

    def __rmul__(self, t):
        return self.__mul__(t)

    def __truediv__(self, t):
        return self.__mul__(1 / t)

    def __abs__(self):
        return np.sqrt(self.length_squared())

    def length(self):
        return abs(self)

    def length_squared(self):
        return self.dot(self)

    def unit(self):
        return self / self.length()

    def dot(self, other):
        return np.dot(self.e, other.e)

    def cross(self, other):
        return np.cross(self.e, other.e)

    def random(self, min=0, max=1):
        return Vec3((random_double(min, max), random_double(min, max), random_double(min, max)))

    def random_in_unit_sphere(self):
        while True:
            p = self.random(-1, 1)
            if p.length_squared() < 1:
                return p

    def random_unit_vector(self):
        return self.random_in_unit_sphere().unit()

    def random_on_hemisphere(self, normal):
        on_unit_sphere = self.random_unit_vector()
        return on_unit_sphere if on_unit_sphere.dot(normal) > 0 else on_unit_sphere * (-1)

    def near_zero(self):
        s = 0.00000001
        return (abs(self.x()) < s) and (abs(self.y()) < s) and (abs(self.z()) < s)

    def reflect(self, other):
        return self - 2 * self.dot(other) * other

    def refract(self, other, eta_ov_eta):

        cos_theta = min(max(self.dot(other), -1.0), 1.0)

        r_out_perp = (self - cos_theta * other) * eta_ov_eta
        r_out_parallel = -np.sqrt(abs(1.0 - r_out_perp.length_squared())) * other
        return r_out_perp + r_out_parallel


Point3 = Vec3

