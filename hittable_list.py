from hittable import Hittable
from hit_record import HitRecord
from interval import Interval
from aabb import AaBb
from sphere import Sphere


class HittableList(Hittable):
    def __init__(self, obj=None):
        self.objects = []
        self.bbox = AaBb()
        if obj:
            self.add(obj)

    def clear(self):
        self.objects.clear()

    def add(self, obj):
        if isinstance(obj, list):
            self.objects.extend(obj)
            for o in obj:
                self.bbox = AaBb(self.bbox, o.bounding_box())
        else:
            self.objects.append(obj)
            self.bbox = AaBb(self.bbox, obj.bounding_box())

    def hit(self, r, ray_t, rec):
        temp_rec = HitRecord()
        hit_anything = False
        closest_so_far = ray_t.max
        objs = self.objects.copy()
        while objs:
            obj = objs.pop()
            if isinstance(obj, Sphere) and obj.bbox.hit(r, Interval(ray_t.min, closest_so_far)):
                if obj.hit(r, Interval(ray_t.min, closest_so_far), temp_rec):
                    hit_anything = True
                    closest_so_far = temp_rec.t

                    rec.p = temp_rec.p
                    rec.normal = temp_rec.normal
                    rec.t = temp_rec.t
                    rec.front_face = temp_rec.front_face
                    rec.mat = temp_rec.mat
                    rec.u = temp_rec.u
                    rec.v = temp_rec.v
            else:
                if obj.bbox.hit(r, Interval(ray_t.min, closest_so_far)):
                    objs.append(obj.left)
                    objs.append(obj.right)


        # for obj in self.objects:
        #     if obj.hit(r, Interval(ray_t.min, closest_so_far), temp_rec):
        #         hit_anything = True
        #         closest_so_far = temp_rec.t
        #
        #         rec.p = temp_rec.p
        #         rec.normal = temp_rec.normal
        #         rec.t = temp_rec.t
        #         rec.front_face = temp_rec.front_face
        #         rec.mat = temp_rec.mat

        return hit_anything

    def bounding_box(self):
        return self.bbox
