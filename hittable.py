from abc import ABC, abstractmethod


class Hittable(ABC):
    @abstractmethod
    def hit(self, r, ray_t, rec):
        pass

    @abstractmethod
    def bounding_box(self):
        pass
