from hit_record import HitRecord
from hittable import Hittable
from vec3 import Vec3


class Sphere(Hittable):

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def hit(self, r, ray_t, rec):

        oc = r.origin() - self.center
        a = r.direction().dot(r.direction())
        half_b = oc.dot(r.direction())
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = half_b * half_b - a * c

        if discriminant < 0:
            return False
        sqrtd = discriminant ** 0.5
        root = (sqrtd + half_b) * (-1) / a
        if not ray_t.surrounds(root):
            root = (sqrtd - half_b) / a
            if not ray_t.surrounds(root):
                return False

        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        return True
