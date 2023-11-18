from hittable import Hittable
import numpy as np


class Sphere(Hittable):

    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, r, ray_t, rec):

        oc = r.origin() - self.center
        a = r.direction().length_squared()
        half_b = oc.dot(r.direction())
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = half_b * half_b - a * c

        if discriminant < 0:
            return False

        sqrtd = np.sqrt(discriminant)
        root = (- sqrtd - half_b) / a
        if not ray_t.surrounds(root):
            root = (sqrtd - half_b) / a
            if not ray_t.surrounds(root):
                return False

        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        rec.mat = self.material
        return True
