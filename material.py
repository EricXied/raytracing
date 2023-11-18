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
    def __init__(self, albedo, fuzz):
        self.albedo = albedo
        self.fuzz = min(1.0, fuzz)

    def scatter(self, r_in, rec, attenuation, scattered):
        reflected = r_in.direction().reflect(rec.normal.unit())

        scattered = Ray(rec.p, reflected + self.fuzz * Vec3().random_unit_vector())
        attenuation = self.albedo
        return attenuation, scattered


class Dielectric(Material):

    def __init__(self, ir):
        self.ir = ir

    def scatter(self, r_in, rec, attenuation, scattered):
        attenuation = Color((1.0, 1.0, 1.0))
        refraction_ratio = 1.0 / self.ir if rec.front_face else self.ir
        unit_direction = r_in.direction().unit()
        refracted = unit_direction.refract(rec.normal, refraction_ratio)
        scattered = Ray(rec.p, refracted)
        return attenuation, scattered