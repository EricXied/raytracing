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
        p = [151, 160, 137, 91, 90, 15, 131, 13, 201, 95, 96, 53, 194, 233, 7, 225,
             140, 36, 103, 30, 69, 142, 8, 99, 37, 240, 21, 10, 23, 190, 6, 148,
             247, 120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32,
             57, 177, 33, 88, 237, 149, 56, 87, 174, 20, 125, 136, 171, 168, 68, 175,
             74, 165, 71, 134, 139, 48, 27, 166, 77, 146, 158, 231, 83, 111, 229, 122,
             60, 211, 133, 230, 220, 105, 92, 41, 55, 46, 245, 40, 244, 102, 143, 54,
             65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132, 187, 208, 89, 18, 169,
             200, 196, 135, 130, 116, 188, 159, 86, 164, 100, 109, 198, 173, 186, 3, 64,
             52, 217, 226, 250, 124, 123, 5, 202, 38, 147, 118, 126, 255, 82, 85, 212,
             207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42, 223, 183, 170, 213,
             119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43, 172, 9,
             129, 22, 39, 253, 19, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112, 104,
             218, 246, 97, 228, 251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241,
             81, 51, 145, 235, 249, 14, 239, 107, 49, 192, 214, 31, 181, 199, 106, 157,
             184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254, 138, 236, 205, 93,
             222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180]
        # p = []
        # for i in range(self.point_count):
        #     p.append(i)
        # Perlin.permute(p, self.point_count)
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
