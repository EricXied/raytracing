from hit_record import HitRecord
from interval import Interval
from utilities import inf, random_double, degree_to_radians
from color import Color
from vec3 import Vec3, Point3
from PIL import Image
from ray import Ray
import numpy as np


class Camera:

    def __init__(self, params_dict):

        self.aspect_ratio = params_dict['aspect_ratio']
        self.image_width = params_dict['image_width']
        self.sample_per_pixel = params_dict['sample_per_pixel']
        self.max_depth = params_dict['max_depth']
        self.vfov = params_dict['vfov']
        self.lookfrom = params_dict['lookfrom']
        self.lookat = params_dict['lookat']
        self.vup = params_dict['vup']
        self.img_name = params_dict['img_name']
        self.defocus_angle = params_dict['defocus_angle']
        self.focus_dist = params_dict['focus_dist']

        self.image_height = int(max(1.0, self.image_width / self.aspect_ratio))
        self.center = self.lookfrom

        # self.focal_length = (self.lookfrom - self.lookat).length()
        self.theta = degree_to_radians(self.vfov)
        self.h = np.tan(self.theta / 2)
        self.viewport_height = 2 * self.h * self.focus_dist
        self.viewport_width = self.viewport_height * (self.image_width / self.image_height)

        self.w = (self.lookfrom - self.lookat).unit()
        self.u = self.vup.cross(self.w).unit()
        self.v = self.w.cross(self.u)

        self.viewport_u = self.viewport_width * self.u
        self.viewport_v = -self.viewport_height * self.v

        self.pixel_delta_u = self.viewport_u / self.image_width
        self.pixel_delta_v = self.viewport_v / self.image_height
        self.viewport_upper_left = self.center - (
                self.focus_dist * self.w) - self.viewport_u / 2 - self.viewport_v / 2
        self.pixel00_loc = self.viewport_upper_left + (self.pixel_delta_u + self.pixel_delta_v) * 0.5

        self.defocus_radius = self.focus_dist * np.tan(degree_to_radians(self.defocus_angle / 2))
        self.defocus_disk_u = self.u * self.defocus_radius
        self.defocus_disk_v = self.v * self.defocus_radius

    def render(self, world, pool):

        im = Image.new("RGB", (self.image_width, self.image_height))
        for j in range(self.image_height):
            print("%.2f percentage..." % (100 * (j * self.image_width) / (self.image_width * self.image_height)))
            row_colors = pool.starmap(self.ray_tracing_task, [(i, j, world) for i in range(self.image_width)])
            for i, color in enumerate(row_colors):

                im.putpixel((i, j), tuple(map(int, (256 * color).e)))

        im.show()
        im.save(self.img_name + '.png')

    def ray_tracing_task(self, i, j, world):

        pixel_color = Color((0, 0, 0))
        for sample in range(self.sample_per_pixel):
            r = self.get_ray(i, j)
            pixel_color += Color(self.ray_color(r, self.max_depth, world))
        pixel_color = Color(pixel_color.e)
        pixel_color = pixel_color.write_color(self.sample_per_pixel)
        return pixel_color

    def ray_color(self, r, depth, world):
        rec = HitRecord()
        if depth <= 0:
            return Color()
        if world.hit(r, Interval(0.0001, inf), rec):
            scattered = Ray()
            attenuation = Color()
            if rec.mat.scatter(r, rec, attenuation, scattered):
                attenuation, scattered = rec.mat.scatter(r, rec, attenuation, scattered)
                return self.ray_color(scattered, depth - 1, world) * attenuation
            return Color()

        unit_direction = Vec3(r.direction()).unit()
        a = 0.5 * (unit_direction.y() + 1.0)
        return (1.0 - a) * Color((1.0, 1.0, 1.0)) + a * Color((0.5, 0.7, 1.0))

    def get_ray(self, i, j):

        pixel_center = self.pixel00_loc + (i * self.pixel_delta_u) + (j * self.pixel_delta_v)
        pixel_sample = pixel_center + self.pixel_sample_square()

        ray_origin = self.center if self.defocus_angle <= 0 else self.defocus_disk_sample()
        ray_direction = pixel_sample - ray_origin

        ray_time = random_double()

        return Ray(ray_origin, ray_direction, ray_time)

    def pixel_sample_square(self):

        px = -0.5 + random_double()
        py = -0.5 + random_double()
        return (px * self.pixel_delta_u) + (py * self.pixel_delta_v)

    def defocus_disk_sample(self):
        p = Vec3().random_in_unit_dist()
        return self.center + (p.x() * self.defocus_disk_u) + (p.y() * self.defocus_disk_v)
