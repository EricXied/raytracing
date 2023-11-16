from hittable import Hittable
from hit_record import HitRecord
from interval import Interval


class HittableList(Hittable):
    def __init__(self):
        self.objects = []

    def clear(self):
        self.objects.clear()

    def add(self, obj):
        self.objects.append(obj)

    def hit(self, r, ray_t, rec):
        temp_rec = HitRecord()
        hit_anything = False
        closest_so_far = ray_t.max
        for obj in self.objects:
            if obj.hit(r, Interval(ray_t.min, closest_so_far), temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.t
                rec.p = temp_rec.p
                rec.t = temp_rec.t
                rec.normal = temp_rec.normal
                rec.mat = temp_rec.mat
        return hit_anything
