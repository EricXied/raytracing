from vec3 import Point3
from hittable_list import HittableList
from sphere import Sphere
from camera import Camera
from material import Lambertian, Metal
from color import Color
from multiprocessing import Pool


def main():
    # World
    num_processes = 8
    pool = Pool(processes=num_processes)

    world = HittableList()
    # world.add(Sphere(Point3((5, 100.5, -50)), 100))
    material_ground = Lambertian(Color((0.8, 0.8, 0.0)))
    material_center = Lambertian(Color((0.7, 0.3, 0.3)))
    material_left = Metal(Color((0.8, 0.8, 0.8)))
    material_right = Metal(Color((0.6, 0.6, 0.6)))

    world.add(Sphere(Point3((0, 0, -1)), 0.5, material_center))
    world.add(Sphere(Point3((0, -100.5, -1)), 100, material_ground))
    world.add(Sphere(Point3((-1, 0, -1)), 0.5, material_left))
    world.add(Sphere(Point3((1, 0, -0.75)), 0.5, material_right))
    # world.add(Sphere(Point3((-0.5, 0, -1)), 0.25, material_center))
    # Camera
    cam = Camera()
    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 400
    cam.sample_per_pixel = 100
    cam.max_depth = 50
    cam.render(world, pool)

    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
