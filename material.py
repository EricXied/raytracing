from abc import ABC, abstractmethod
from ray import Ray
from vec3 import Vec3
from color import Color
import numpy as np



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
        scattered = Ray(rec.p, scatter_direction, r_in.time())
        attenuation = self.albedo.value(rec.u, rec.v, rec.p)
        return attenuation, scattered


class Metal(Material):
    def __init__(self, albedo, fuzz):
        self.albedo = albedo
        self.fuzz = min(1.0, fuzz)

    def scatter(self, r_in, rec, attenuation, scattered):
        reflected = r_in.direction().reflect(rec.normal.unit())

        scattered = Ray(rec.p, reflected + self.fuzz * Vec3().random_unit_vector(), r_in.time())
        attenuation = self.albedo
        return attenuation, scattered


class Dielectric(Material):

    def __init__(self, ir):
        self.ir = ir

    def scatter(self, r_in, rec, attenuation, scattered):
        attenuation = Color((1.0, 1.0, 1.0))

        refraction_ratio = 1.0 / self.ir if rec.front_face else self.ir
        unit_direction = r_in.direction().unit()
        cos_theta = min(max(-unit_direction.dot(rec.normal), -1.0), 1.0)
        sin_theta = np.sqrt(1 - cos_theta * cos_theta)
        cannot_reflect = refraction_ratio * sin_theta > 1.0

        if cannot_reflect:
            direction = unit_direction.reflect(rec.normal)
        else:
            direction = unit_direction.refract(rec.normal, refraction_ratio)

        scattered = Ray(rec.p, direction, r_in.time())
        return attenuation, scattered
