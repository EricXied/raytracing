from hittable import Hittable
import numpy as np
from vec3 import Vec3
from aabb import AaBb


class Sphere(Hittable):

    def __init__(self, center1, radius, material, center2=None):
        self.center1 = center1
        self.radius = radius
        self.material = material
        self.is_moving = center2 is not None
        rvec = Vec3((radius, radius, radius))
        if self.is_moving:
            self.center_vec = center2 - center1
            box1 = AaBb(center1 - rvec, center1 + rvec)
            box2 = AaBb(center2 - rvec, center2 + rvec)
            self.bbox = AaBb(box1, box2)
        else:
            self.bbox = AaBb(center1 - rvec, center1 + rvec)

    def hit(self, r, ray_t, rec):

        center = self.center(r.time()) if self.is_moving else self.center1
        oc = r.origin() - center
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
        outward_normal = (rec.p - self.center1) / self.radius
        rec.set_face_normal(r, outward_normal)
        rec.mat = self.material
        return True

    def center(self, time):
        return self.center1 + time * self.center_vec

    def bounding_box(self):
        return self.bbox
