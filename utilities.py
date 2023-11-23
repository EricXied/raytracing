import numpy as np

pi = np.pi
inf = np.inf
floor = np.floor


def degree_to_radians(degrees):
    return degrees * pi / 180


def random_double(minr=0, maxr=1):
    return (maxr - minr) * np.random.random_sample() + minr


def random_int(minr=0, maxr=1):
    return np.random.randint(minr, maxr)
