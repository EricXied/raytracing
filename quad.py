from aabb import AaBb
from hittable import Hittable


class Quad(Hittable):
    def __init__(self, q, u, v, m):
        self.q = q
        self.u = u
        self.v = v
        self.mat = m
        self.bbox = AaBb(q, q + u + v)
        self.bbox.pad()
        n = u.cross(v)
        self.normal = u.cross(v).unit()
        self.d = self.normal.dot(q)
        self.w = n / n.dot(n)


    def bounding_box(self):
        return self.bbox


    def hit(self, r, ray_t, rec):
        denom = self.normal.dot(r.direction())
        if abs(denom) < 0.00000001:
            return False

        t = (self.d - self.normal.dot(r.origin())) / denom
        if not ray_t.contains(t):
            return False

        intersection = r.at(t)
        planar_hitpt_vector = intersection - self.q
        alpha = self.w.dot(planar_hitpt_vector.cross(self.v))
        beta = self.w.dot(self.u.cross(planar_hitpt_vector))
        if not self.is_interior(alpha, beta, rec):
            return False

        rec.t = t
        rec.p = intersection
        rec.mat = self.mat
        rec.set_face_normal(r, self.normal)
        return True


    def is_interior(self, a, b, rec):
        if a < 0 or a > 1 or b < 0 or b > 1:
            return False
        rec.u = a
        rec.v = a
        return True
