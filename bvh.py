from hittable import Hittable
from hittable_list import HittableList
from aabb import AaBb
import random
from interval import Interval
from sphere import Sphere


class BvhNode(Hittable):
    def __init__(self, src_objects):
        self.objects = src_objects
        axis = random.randint(0, 2)

        comparator = [BvhNode.box_x_compare, BvhNode.box_y_compare, BvhNode.box_z_compare][axis]
        object_span = len(src_objects)

        if object_span == 1:
            self.left = self.right = self.objects[0]
        elif object_span == 2:
            self.objects = sorted(self.objects, key=lambda obj: comparator(obj))
            self.left = self.objects[0]
            self.right = self.objects[1]
        else:
            self.objects = sorted(self.objects, key=lambda obj: comparator(obj))
            mid = object_span // 2
            self.left = BvhNode(self.objects[:mid])
            self.right = BvhNode(self.objects[mid:])
        self.bbox = AaBb(self.left.bounding_box(), self.right.bounding_box())

    def hit(self, r, ray_t, rec):

        if not self.bbox.hit(r, ray_t):
            return False
        hit_left = self.left.hit(r, ray_t, rec)
        m_bound = rec.t if hit_left else ray_t.max
        hit_right = self.right.hit(r, Interval(ray_t.min, m_bound), rec)

        return hit_left or hit_right

    def bounding_box(self):
        return self.bbox

    @staticmethod
    def box_compare(a, axis_index):
        return a.bounding_box().axis(axis_index).min

    @staticmethod
    def box_x_compare(a):
        return BvhNode.box_compare(a, 0)

    @staticmethod
    def box_y_compare(a):
        return BvhNode.box_compare(a, 1)

    @staticmethod
    def box_z_compare(a):
        return BvhNode.box_compare(a, 2)
