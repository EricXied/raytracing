from utilities import random_double, random_int, floor
from vec3 import Vec3


class Perlin:
    def __init__(self):
        self.point_count = 256

        self.ranvec = []
        for i in range(self.point_count):
            self.ranvec.append(Vec3().random(-1, 1).unit())
        self.perm_x = self.perlin_generate_perm()
        self.perm_y = self.perlin_generate_perm()
        self.perm_z = self.perlin_generate_perm()

    def __del__(self):
        del self.ranvec
        del self.perm_x
        del self.perm_y
        del self.perm_z

    def turb(self, p, depth=7):
        accum = 0.0
        temp_p = p
        weight = 1.0
        for i in range(depth):
            accum += weight * self.noise(temp_p)
            weight *= 0.5
            temp_p *= 2
        return abs(accum)

    def noise(self, p):
        u = p.x() - floor(p.x())
        v = p.y() - floor(p.y())
        w = p.z() - floor(p.z())

        i = int(floor(p.x()))
        j = int(floor(p.y()))
        k = int(floor(p.z()))

        c = [[[0] * 2 for _ in range(2)] for _ in range(2)]
        for di in range(2):
            for dj in range(2):
                for dk in range(2):
                    c[di][dj][dk] = self.ranvec[
                        self.perm_x[(i + di) & 255] ^ self.perm_y[(j + dj) & 255] ^ self.perm_z[(k + dk) & 255]]

        return Perlin.trilinear_interp(c, u, v, w)

    def perlin_generate_perm(self):
        p = []
        for i in range(self.point_count):
            p.append(i)
        Perlin.permute(p, self.point_count)
        return p

    @staticmethod
    def trilinear_interp(c, u, v, w):
        uu = u * u * (3 - 2 * u)
        vv = v * v * (3 - 2 * v)
        ww = w * w * (3 - 2 * w)
        accum = 0.0
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    accum += (i * uu + (1 - i) * (1 - uu)) * (j * vv + (1 - j) * (1 - vv)) * (
                            k * ww + (1 - k) * (1 - ww)) * \
                             c[i][j][k].dot(Vec3((u - i, v - j, w - k)))
        return accum

    @staticmethod
    def permute(p, n):
        for i in range(n - 1, 0, -1):
            target = random_int(0, i)
            p[i], p[target] = p[target], p[i]
