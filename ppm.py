from vec3 import Point3
from hittable_list import HittableList
from sphere import Sphere
from camera import Camera
from material import Lambertian, Metal, Dielectric
from color import Color
from multiprocessing import Pool


def main():
    # World
    num_processes = 8
    pool = Pool(processes=num_processes)

    world = HittableList()

    material_ground = Lambertian(Color((0.8, 0.8, 0.0)))
    material_center = Dielectric(1.5)
    material_left = Dielectric(1.5)
    material_right = Metal(Color((0.8, 0.6, 0.2)), 1)

    world.add(Sphere(Point3((0, 0, -1)), 0.5, material_center))
   # world.add(Sphere(Point3((0, -100.5, -1)), 100, material_ground))
    world.add(Sphere(Point3((-1, 0, -1)), 0.5, material_left))
    #world.add(Sphere(Point3((1, 0, -1)), 0.5, material_right))
    world.add(Sphere(Point3((0, 0, -2)), 0.5, material_right))
    # Camera
    cam = Camera()
    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 200
    cam.sample_per_pixel = 10
    cam.max_depth = 50
    cam.render(world, pool)

    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
