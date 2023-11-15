import numpy as np


class Vec3:
    def __init__(self, e=(0, 0, 0)):
        try:
            self.e = e.e
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

        return Vec3(self.e * t)

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


# a = Vec3((1, 1, 1))
# b = Vec3((1, 1, 2))
# print(a * np.array(1.1))

Point3 = Vec3
