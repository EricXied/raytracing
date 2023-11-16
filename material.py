from abc import ABC, abstractmethod
from ray import Ray
from vec3 import Vec3
from color import Color


class Material(ABC):
    @abstractmethod
    def scatter(self, r_in, rec, attenuation, scattered):
        pass


class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, r_in, rec, attenuation, scattered):
        scatter_direction = rec.normal + Vec3().random_unit_vector()
        if scatter_direction.near_zero():
            scatter_direction = rec.normal
        scattered = Ray(rec.p, scatter_direction)
        attenuation = self.albedo
        return attenuation, scattered


class Metal(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, r_in, rec, attenuation, scattered):
        # print(r_in.direction())
        reflected = r_in.direction().reflect(rec.normal.unit())
        scattered = Ray(rec.p, reflected)
        attenuation = self.albedo
        return attenuation, scattered
