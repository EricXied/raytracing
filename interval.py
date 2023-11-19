import numpy as np


class Interval:

    def __init__(self, mi, mx):
        self.min = mi
        self.max = mx

    def contains(self, x):
        return self.min <= x <= self.max

    def surrounds(self, x):
        return self.min < x < self.max

    def clamp(self, x):
        if x < self.min: return self.min
        if x > self.max: return self.max
        return x


empty = Interval(np.inf, -np.inf)
universe = Interval(-np.inf, np.inf)
