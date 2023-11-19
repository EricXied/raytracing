from vec3 import Point3, Vec3
from hittable_list import HittableList
from sphere import Sphere
from camera import Camera
from material import Lambertian, Metal, Dielectric
from color import Color
from multiprocessing import Pool
from utilities import random_double


def main():
    num_processes = 8
    pool = Pool(processes=num_processes)

    # World
    world = HittableList()

    material_ground = Lambertian(Color((0.5, 0.5, 0.5)))
    world.add(Sphere(Point3((0, -1000, 0)), 1000, material_ground))

    for i in range(-11, 11):
        for j in range(-11, 11):
            choose_mat = random_double()
            center = Point3((i + 0.9 * random_double(), 0.2, j + 0.9 * random_double()))
            if ((center - Point3((4, 0.2, 0))).length() > 0.9):

                if choose_mat < 0.8:
                    albedo = Color().random() * Color().random()
                    sphere_material = Lambertian(albedo)
                    world.add(Sphere(center, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    albedo = Color().random(0.5, 1)
                    fuzz = random_double(0, 0.5)
                    sphere_material = Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                else:
                    sphere_material = Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))

    material1 = Dielectric(1.5)
    world.add(Sphere(Point3((0, 1, 0)), 1.0, material1))

    material2 = Lambertian(Color((0.4, 0.2, 0.1)))
    world.add(Sphere(Point3((-4, 1, 0)), 1.0, material2))

    material3 = Metal(Color((0.7, 0.6, 0.5)), 0.0)
    world.add(Sphere(Point3((4, 1, 0)), 1.0, material3))

    # Camera
    camera_param = {'aspect_ratio': 16.0 / 9.0,
                    'image_width': 1200,
                    'sample_per_pixel': 50,
                    'max_depth': 50,
                    'vfov': 20,
                    'lookfrom': Point3((13, 2, 3)),
                    'lookat': Point3((0, 0, 0)),
                    'vup': Vec3((0, 1, 0)),
                    'img_name': 'Final Scene2',
                    'defocus_angle': 0.6,
                    'focus_dist': 10
                    }

    cam = Camera(camera_param)
    # cam.aspect_ratio = 16.0 / 9.0
    # cam.image_width = 200
    # cam.sample_per_pixel = 10
    # cam.max_depth = 50
    #
    # cam.vfov = 90
    # cam.lookfrom = Point3((-2, 2, 1))
    # cam.lookat = Point3((0, 0, -1))
    # cam.vup = Vec3((0, 1, 0))

    cam.render(world, pool)

    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
