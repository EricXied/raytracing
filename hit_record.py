class HitRecord:
    def __init__(self, p=None, normal=None, t=None, f=None):
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = f

    def set_face_normal(self, r, outward_normal):
        self.front_face = r.direction().dot(outward_normal) < 0
        self.normal = outward_normal if self.front_face else outward_normal*(-1)
