from abc import ABC, abstractmethod


class Hittable(ABC):
    @abstractmethod
    def hit(self, r, ray_tmin, ray_tmax, rec):
        pass
