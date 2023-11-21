from vec3 import Point3, Vec3
from hittable_list import HittableList
from sphere import Sphere
from camera import Camera
from material import Lambertian, Metal, Dielectric
from color import Color
from multiprocessing import Pool
from utilities import random_double
from bvh import BvhNode


def main():
    num_processes = 8
    pool = Pool(processes=num_processes)

    # World
    world = []
    material_ground = Lambertian(Color((0.5, 0.5, 0.5)))

    world.append(Sphere(Point3((0, -1000, 0)), 1000, material_ground))

    for i in range(-11, 11):
        for j in range(-11, 11):
            choose_mat = random_double()
            center = Point3((i + 0.9 * random_double(), 0.2, j + 0.9 * random_double()))
            if (center - Point3((4, 0.2, 0))).length() > 0.9:

                if choose_mat < 0.8:
                    albedo = Color().random() * Color().random()
                    sphere_material = Lambertian(albedo)
                    center2 = center + Vec3((0, random_double(0, 0.5), 0))
                    world.append(Sphere(center, 0.2, sphere_material, center2))
                    #world.append(Sphere(center, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    albedo = Color().random(0.5, 1)
                    fuzz = random_double(0, 0.5)
                    sphere_material = Metal(albedo, fuzz)
                    world.append(Sphere(center, 0.2, sphere_material))
                else:
                    sphere_material = Dielectric(1.5)
                    world.append(Sphere(center, 0.2, sphere_material))

    center = Point3((2 + 0.9 * random_double(), 0.2, 2 + 0.9 * random_double()))
    albedo = Color().random(0.5, 1)
    fuzz = random_double(0, 0.5)
    sphere_material = Metal(albedo, fuzz)
    world.append(Sphere(center, 0.2, sphere_material))

    material1 = Dielectric(1.5)
    world.append(Sphere(Point3((-2, 1, 0)), 1.0, material1))

    material2 = Lambertian(Color((0.4, 0.2, 0.1)))
    # world.append(Sphere(Point3((0, 1, 0)), 1.0, material2))

    world.append(Sphere(Point3((-6, 1, -1)), 1.0, material2))

    material3 = Metal(Color((0.7, 0.6, 0.5)), 0.0)
    world.append(Sphere(Point3((1, 1, -1)), 1.0, material3))

    #world = HittableList(world)
    world = HittableList(BvhNode(world))

    # Camera
    camera_param = {'aspect_ratio': 16.0 / 9.0,
                    'image_width': 400,
                    'sample_per_pixel': 100,
                    'max_depth': 50,
                    'vfov': 40,
                    'lookfrom': Point3((13, 2, 3)),
                    'lookat': Point3((0, 0, 0)),
                    'vup': Vec3((0, 1, 0)),
                    'img_name': 'Final Scene4',
                    'defocus_angle': 0.6,
                    'focus_dist': 10
                    }

    cam = Camera(camera_param)

    cam.render(world, pool)

    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
