from interval import Interval
from vec3 import Point3, Vec3


class AaBb:

    def __init__(self, a=None, b=None):
        if isinstance(a, (Point3, Vec3)) and isinstance(b, (Point3, Vec3)):
            self.x = Interval(min(a.e[0], b.e[0]), max(a.e[0], b.e[0]))
            self.y = Interval(min(a.e[1], b.e[1]), max(a.e[1], b.e[1]))
            self.z = Interval(min(a.e[2], b.e[2]), max(a.e[2], b.e[2]))
        elif isinstance(a, AaBb) and isinstance(b, AaBb):
            self.x = Interval(a.x, b.x)
            self.y = Interval(a.y, b.y)
            self.z = Interval(a.z, b.z)
        elif a is None and b is None:
            self.x = Interval()
            self.y = Interval()
            self.z = Interval()
        else:
            raise ValueError("Invalid arguments provided for aabb constructor")
        self.interval = [self.x.min, self.x.max, self.y.min, self.y.max, self.z.min, self.z.max]

    def pad(self):
        delta = 0.0001
        self.x = self.x if self.x.size() >= delta else self.x.expand(delta)
        self.y = self.y if self.y.size() >= delta else self.y.expand(delta)
        self.z = self.z if self.z.size() >= delta else self.z.expand(delta)

    def axis(self, n):
        return [self.x, self.y, self.z][n]

    def hit(self, r, ray_t):

        # for i in range(3):
        #     t0 = min((self.axis(i).min - r.origin().e[i]) / r.direction().e[i],
        #              (self.axis(i).max - r.origin().e[i]) / r.direction().e[i])
        #     t1 = max((self.axis(i).min - r.origin().e[i]) / r.direction().e[i],
        #              (self.axis(i).max - r.origin().e[i]) / r.direction().e[i])
        #     ray_t.min = max(t0, ray_t.min)
        #     ray_t.max = min(t1, ray_t.max)
        #     if ray_t.max <= ray_t.min:
        #         return False
        # return True
        for i in range(3):

            invD = 1 / r.direction().e[i]
            orig = r.origin().e[i]

            t0 = (self.axis(i).min - orig) * invD
            t1 = (self.axis(i).max - orig) * invD

            if invD < 0:
                t0, t1 = t1, t0
            if t0 > ray_t.min:
                ray_t.min = t0
            if t1 < ray_t.max:
                ray_t.max = t1

            if ray_t.max <= ray_t.min:
                return False
        return True
