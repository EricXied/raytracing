from PIL import Image
from color import Color
from ray import Ray
from vec3 import Vec3, Point3
from hit_record import HitRecord
from utilities import pi, inf, degree_to_radians
from hittable_list import HittableList
from sphere import Sphere
from interval import Interval
from camera import Camera

def ray_color(r, world):
    rec = HitRecord()
    if world.hit(r, Interval(0, inf), rec):
        return 0.5 * (rec.normal + Color((1, 1, 1)))

    unit_direction = Vec3(r.direction()).unit()
    a = 0.5 * (unit_direction.y() + 1.0)

    return (1.0 - a) * Color((1.0, 1.0, 1.0)) + a * Color((0.5, 0.7, 1.0))

# def hit_sphere(center, radius, r):
#     oc = r.origin() - center
#     a = r.direction().dot(r.direction())
#     half_b = oc.dot(r.direction())
#     c = oc.dot(oc) - radius * radius
#     discriminant = half_b * half_b - a * c
#     if discriminant < 0:
#         return -1.0
#     else:
#         return (-discriminant ** 0.5 - half_b) / a

def write_color(image, x, y, pixel):
    image.putpixel((x, y), tuple(map(int, (256 * pixel).e)))


def main():
    # Image
    # aspect_ratio = 16.0 / 9.0
    # image_width = 400
    # image_height = int(max(1, image_width / aspect_ratio))

    # World
    world = HittableList()
    world.add(Sphere(Point3((0, 0, -1)), 0.5))
    world.add(Sphere(Point3((0, -100.5, -1)), 100))
    # Camera

    cam = Camera()
    cam.aspect_ratio = 16.0/9.0
    cam.image_width = 400
    cam.render(world)

    # data = [0] * image_width * image_height
    # im = Image.new("RGB", (image_width, image_height))
    # for j in range(int(image_height)):
    #     for i in range(image_width):
    #         pixel_center = pixel00_loc + (i * pixel_delta_u) + (j * pixel_delta_v)
    #         ray_direction = pixel_center - camera_center
    #
    #         r = Ray(camera_center, ray_direction)
    #         pixel_color = ray_color(r, world)
    #         # write_color(im, i, j, pixel_color)
    #         # im.putpixel((i, j), tuple(map(int, (256 * pixel_color).e)))
    #         data[j * image_width + i] = tuple(map(int, (256 * pixel_color).e))
    #
    # im.putdata(data)
    # im.show()


main()
