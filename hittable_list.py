from hittable import Hittable
from hit_record import HitRecord


class HittableList(Hittable):
    def __init__(self):
        self.objects = []

    def clear(self):
        self.objects.clear()

    def add(self, obj):
        self.objects.append(obj)

    def hit(self, r, ray_tmin, ray_tmax, rec):
        temp_rec = HitRecord()
        hit_anything = False
        closet_so_far = ray_tmax
        for obj in self.objects:
            if obj.hit(r, ray_tmin, closet_so_far, temp_rec):
                hit_anything = True
                closet_so_far = temp_rec.t
                rec.t = temp_rec.t
                rec.normal = temp_rec.normal
        return hit_anything
