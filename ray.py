class Ray:
    def __init__(self, point3, vec3):
        self.point3 = point3
        self.vec3 = vec3

    def at(self, t):
        return self.point3 + t * self.vec3

    def direction(self):
        return self.vec3

    def origin(self):
        return self.point3
