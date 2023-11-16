from vec3 import Vec3, Point3
from material import Lambertian
from color import Color
class HitRecord:
    def __init__(self, mat=Lambertian(Color()), p=Point3(), normal=Vec3(), t=0, f=False):
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = f
        self.mat = mat

    def set_face_normal(self, r, outward_normal):
        self.front_face = r.direction().dot(outward_normal) < 0
        self.normal = outward_normal if self.front_face else outward_normal * (-1)
