from hit_record import HitRecord
from interval import Interval
from utilities import inf, random_double
from color import Color
from vec3 import Vec3, Point3
from PIL import Image
from ray import Ray


class Camera:

    def __init__(self):
        self.aspect_ratio = 1.0
        self.image_width = 100
        self.sample_per_pixel = 10
        self.max_depth = 10

        self.image_height = int(max(1.0, self.image_width / self.aspect_ratio))
        self.focal_length = 1.0
        self.viewport_height = 2.0
        self.viewport_width = self.viewport_height * (self.image_width / self.image_height)
        self.camera_center = Point3((0, 0, 0))
        self.viewport_u = Vec3((self.viewport_width, 0, 0))
        self.viewport_v = Vec3((0, -self.viewport_height, 0))
        self.pixel_delta_u = self.viewport_u / self.image_width
        self.pixel_delta_v = self.viewport_v / self.image_height
        self.viewport_upper_left = self.camera_center - Vec3(
            (0, 0, self.focal_length)) - self.viewport_u / 2 - self.viewport_v / 2
        self.pixel00_loc = self.viewport_upper_left + (self.pixel_delta_u + self.pixel_delta_v) * 0.5

    # def render(self, world):
    #     self.initialize()
    #
    #     im = Image.new("RGB", (self.image_width, self.image_height))
    #     for j in range(self.image_height):
    #         print("%.2f percentage..." % (100 * (j * self.image_width) / (self.image_width * self.image_height)))
    #         for i in range(self.image_width):
    #             pixel_color = Color((0, 0, 0))
    #             for sample in range(self.sample_per_pixel):
    #                 r = self.get_ray(i, j)
    #                 pixel_color += Color(self.ray_color(r, self.max_depth, world))
    #             pixel_color = Color(pixel_color.e)
    #             pixel_color = pixel_color.write_color(self.sample_per_pixel)
    #             im.putpixel((i, j), tuple(map(int, (256 * pixel_color).e)))
    #         # im.show()
    #     im.show()
    #     im.save('MetalDiffuse.png')
    def initialize(self):
        self.focal_length = 1.0
        self.viewport_height = 2.0
        self.image_height = int(max(1, self.image_width / self.aspect_ratio))
        self.viewport_width = self.viewport_height * (self.image_width / self.image_height)
        self.camera_center = Point3((0, 0, 0))
        self.viewport_u = Vec3((self.viewport_width, 0, 0))
        self.viewport_v = Vec3((0, -self.viewport_height, 0))
        self.pixel_delta_u = self.viewport_u / self.image_width
        self.pixel_delta_v = self.viewport_v / self.image_height
        self.viewport_upper_left = self.camera_center - Vec3(
            (0, 0, self.focal_length)) - self.viewport_u / 2 - self.viewport_v / 2
        self.pixel00_loc = self.viewport_upper_left + (self.pixel_delta_u + self.pixel_delta_v) * 0.5

    def render(self, world, pool):
        self.initialize()

        im = Image.new("RGB", (self.image_width, self.image_height))
        for j in range(self.image_height):
            print("%.2f percentage..." % (100 * (j * self.image_width) / (self.image_width * self.image_height)))
            row_colors = pool.starmap(self.ray_tracing_task, [(i, j, world) for i in range(self.image_width)])
            for i, color in enumerate(row_colors):
                im.putpixel((i, j), tuple(map(int, (256 * color).e)))

        im.show()
        im.save('Refraction3.png')

    def ray_tracing_task(self, i, j, world):

        pixel_color = Color((0, 0, 0))
        for sample in range(self.sample_per_pixel):
            r = self.get_ray(i, j)
            pixel_color += Color(self.ray_color(r, self.max_depth, world))
        pixel_color = Color(pixel_color.e)
        pixel_color = pixel_color.write_color(self.sample_per_pixel)
        return pixel_color

    def ray_color(self, r, depth, world):
        rec = [HitRecord()]
        if depth <= 0:
            return Color()
        if world.hit(r, Interval(0.0001, inf), rec):
            scattered = Ray()
            attenuation = Color()
            if rec[0].mat.scatter(r, rec[0], attenuation, scattered):
                # if rec.front_face:
                #     print("yes")
                attenuation, scattered = rec[0].mat.scatter(r, rec[0], attenuation, scattered)
                return self.ray_color(scattered, depth - 1, world) * attenuation
            return Color()

        unit_direction = Vec3(r.direction()).unit()
        a = 0.5 * (unit_direction.y() + 1.0)
        return (1.0 - a) * Color((1.0, 1.0, 1.0)) + a * Color((0.5, 0.7, 1.0))

    def get_ray(self, i, j):

        pixel_center = self.pixel00_loc + (i * self.pixel_delta_u) + (j * self.pixel_delta_v)
        pixel_sample = pixel_center + self.pixel_sample_square()

        ray_origin = self.camera_center
        ray_direction = pixel_sample - ray_origin

        return Ray(ray_origin, ray_direction)

    def pixel_sample_square(self):

        px = -0.5 + random_double()
        py = -0.5 + random_double()
        return (px * self.pixel_delta_u) + (py * self.pixel_delta_v)
