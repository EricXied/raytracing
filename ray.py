from vec3 import Point3, Vec3


class Ray:
    def __init__(self, point3=Point3(), vec3=Vec3(), time=0):
        self.point3 = point3
        self.vec3 = vec3
        self.tm = time

    def at(self, t):
        return self.point3 + t * self.vec3

    def direction(self):
        return self.vec3

    def origin(self):
        return self.point3

    def time(self):
        return self.tm
