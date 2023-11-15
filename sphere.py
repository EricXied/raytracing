from hit_record import HitRecord
from hittable import Hittable
from vec3 import Vec3


class Sphere(Hittable):

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def hit(self, r, ray_tmin, ray_tmax, rec):
        oc = r.origin() - self.center
        a = r.direction().length_squared()
        half_b = oc.dot(r.direction())
        c = oc.length_squared() - self.radius * self.radius
        discriminant = half_b * half_b - a * c

        # oc = r.origin() - self.center
        # a = r.direction().dot(r.direction())
        # half_b = oc.dot(r.direction())
        # c = oc.dot(oc) - self.radius * self.radius
        # discriminant = half_b * half_b - a * c

        if discriminant < 0:
            return False
        sqrtd = discriminant ** 0.5
        root = (-sqrtd - half_b) / a
        if root <= ray_tmin or ray_tmax <= root:
            root = (sqrtd - half_b) / a
            if root <= ray_tmin or ray_tmax <= root:
                return False

        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        return True
