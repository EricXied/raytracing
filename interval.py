import numpy as np


class Interval:

    def __init__(self, a=None, b=None):
        if isinstance(a, (np.int32, int, float)) and isinstance(b, (np.int32, int, float)):
            self.min = a
            self.max = b
        elif isinstance(a, Interval) and isinstance(b, Interval):
            self.min = min(a.min, b.min)
            self.max = max(a.max, b.max)
        elif a is None and b is None:
            self.min = np.inf
            self.max = -np.inf
        else:
            raise ValueError("Invalid arguments provided for Interval constructor")

    def contains(self, x):
        return self.min <= x <= self.max

    def surrounds(self, x):
        return self.min < x < self.max

    def clamp(self, x):
        if x < self.min:
            return self.min
        if x > self.max:
            return self.max
        return x

    def size(self):
        return self.max - self.min

    def expand(self, delta):
        padding = delta / 2
        return Interval(self.min - padding, self.max + padding)


empty = Interval(np.inf, -np.inf)
universe = Interval(-np.inf, np.inf)
