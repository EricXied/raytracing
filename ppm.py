from vec3 import Point3, Vec3
from hittable_list import HittableList
from sphere import Sphere
from camera import Camera
from material import Lambertian, Metal, Dielectric, DiffuseLight
from color import Color
from multiprocessing import Pool
from utilities import random_double
from bvh import BvhNode
from texture import CheckerTexture, ImageTexture, NoiseTexture
from quad import Quad


def random_spheres(pool):
    # World
    world = []
    material_ground = Lambertian(Color((0.5, 0.5, 0.5)))
    world.append(Sphere(Point3((0, -1000, 0)), 1000, material_ground))

    for i in range(-1, 1):
        for j in range(-1, 1):
            choose_mat = random_double()
            center = Point3((i + 0.9 * random_double(), 0.2, j + 0.9 * random_double()))
            if (center - Point3((4, 0.2, 0))).length() > 0.9:

                if choose_mat < 0.8:
                    albedo = Color(Color().random() * Color().random())
                    sphere_material = Lambertian(albedo)
                    center2 = center + Vec3((0, random_double(0, 0.5), 0))
                    world.append(Sphere(center, 0.2, sphere_material, center2))
                    # world.append(Sphere(center, 0.2, sphere_material))
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

    # world = HittableList(world)
    world = HittableList(BvhNode(world))

    # Camera
    camera_param = {'aspect_ratio': 16.0 / 9.0,
                    'image_width': 400,
                    'sample_per_pixel': 1,
                    'max_depth': 50,
                    'vfov': 40,
                    'lookfrom': Point3((13, 2, 3)),
                    'lookat': Point3((0, 0, 0)),
                    'vup': Vec3((0, 1, 0)),
                    'img_name': 'Final Scene4',
                    'defocus_angle': 0.6,
                    'focus_dist': 10,
                    'background': Color((0.7, 0.8, 1.0))
                    }

    cam = Camera(camera_param)
    cam.render(world, pool)


def two_sphere(pool):
    world = []
    checker = Lambertian(CheckerTexture(0.8, Color((0.2, 0.3, 0.1)), Color((0.9, 0.9, 0.9))))
    world.append(Sphere(Point3((0, -20, 0)), 20, checker))
    world.append(Sphere(Point3((0, 20, 0)), 20, checker))

    world = HittableList(BvhNode(world))
    # Camera
    camera_param = {'aspect_ratio': 16.0 / 9.0,
                    'image_width': 400,
                    'sample_per_pixel': 10,
                    'max_depth': 50,
                    'vfov': 50,
                    'lookfrom': Point3((13, 2, 3)),
                    'lookat': Point3((0, 0, 0)),
                    'vup': Vec3((0, 1, 0)),
                    'img_name': 'TwoSpheres',
                    'defocus_angle': 0,
                    'focus_dist': 10,
                    'background': Color((0.7, 0.8, 1.0))
                    }

    cam = Camera(camera_param)
    cam.render(world, pool)


def earth(pool):
    world = []

    earth_texture = ImageTexture('earthmap.jpg')
    earth_surface = Lambertian(earth_texture)
    globe = Sphere(Point3((0, 0, 0)), 2, earth_surface)
    world.append(globe)
    world = HittableList(BvhNode(world))
    # Camera
    camera_param = {'aspect_ratio': 16.0 / 9.0,
                    'image_width': 400,
                    'sample_per_pixel': 10,
                    'max_depth': 50,
                    'vfov': 20,
                    'lookfrom': Point3((0, 0, 12)),
                    'lookat': Point3((0, 0, 0)),
                    'vup': Vec3((0, 1, 0)),
                    'img_name': 'Earth',
                    'defocus_angle': 0,
                    'focus_dist': 10,
                    'background': Color((0.7, 0.8, 1.0))
                    }

    cam = Camera(camera_param)
    cam.render(world, pool)


def two_perlin_spheres(pool):
    world = []

    pertext = NoiseTexture(4)

    world.append(Sphere(Point3((0, -1000, 0)), 1000, Lambertian(pertext)))
    world.append(Sphere(Point3((0, 2, 0)), 2, Lambertian(pertext)))

    world = HittableList(BvhNode(world))
    # Camera
    camera_param = {'aspect_ratio': 16.0 / 9.0,
                    'image_width': 400,
                    'sample_per_pixel': 1,
                    'max_depth': 50,
                    'vfov': 20,
                    'lookfrom': Point3((13, 2, 3)),
                    'lookat': Point3((0, 0, 0)),
                    'vup': Vec3((0, 1, 0)),
                    'img_name': 'Marble2',
                    'defocus_angle': 0,
                    'focus_dist': 10
                    }

    cam = Camera(camera_param)
    cam.render(world, pool)


def quads(pool):
    world = []

    left_red = Lambertian(Color((1.0, 0.2, 0.2)))
    back_green = Lambertian(Color((0.2, 1.0, 0.2)))
    right_blue = Lambertian(Color((0.2, 0.2, 1.0)))
    upper_orange = Lambertian(Color((1.0, 0.5, 0.0)))
    lower_teal = Lambertian(Color((0.2, 0.8, 0.8)))

    world.append(Quad(Point3((-3, -2, 5)), Vec3((0, 0, -4)), Vec3((0, 4, 0)), left_red))
    world.append(Quad(Point3((-2, -2, 0)), Vec3((4, 0, 0)), Vec3((0, 4, 0)), back_green))
    world.append(Quad(Point3((3, -2, 1)), Vec3((0, 0, 4)), Vec3((0, 4, 0)), right_blue))
    world.append(Quad(Point3((-2, 3, 1)), Vec3((4, 0, 0)), Vec3((0, 0, 4)), upper_orange))
    world.append(Quad(Point3((-2, -3, 5)), Vec3((4, 0, 0)), Vec3((0, 0, -4)), lower_teal))

    world = HittableList(BvhNode(world))
    # Camera
    camera_param = {'aspect_ratio': 1,
                    'image_width': 400,
                    'sample_per_pixel': 10,
                    'max_depth': 50,
                    'vfov': 80,
                    'lookfrom': Point3((0, 0, 9)),
                    'lookat': Point3((0, 0, 0)),
                    'vup': Vec3((0, 1, 0)),
                    'img_name': 'Quads',
                    'defocus_angle': 0,
                    'focus_dist': 10,
                    'background': Color((0.7, 0.8, 1.0))
                    }

    cam = Camera(camera_param)
    cam.render(world, pool)


def simple_light(pool):
    world = []
    pertext = NoiseTexture(4)

    world.append(Sphere(Point3((0, -1000, 0)), 1000, Lambertian(pertext)))
    world.append(Sphere(Point3((0, 2, 0)), 2, Lambertian(pertext)))

    difflight = DiffuseLight(Color(4, 4, 4))
    world.append(Quad(Point3((3, 1, -2)), Vec3((2, 0, 0)), Vec3((0, 2, 0)), difflight))
    world = HittableList(BvhNode(world))
    # Camera
    camera_param = {'aspect_ratio': 16.0 / 9.0,
                    'image_width': 400,
                    'sample_per_pixel': 100,
                    'max_depth': 50,
                    'vfov': 20,
                    'lookfrom': Point3((26, 3, 6)),
                    'lookat': Point3((0, 2, 0)),
                    'vup': Vec3((0, 1, 0)),
                    'img_name': 'LightSource',
                    'defocus_angle': 0,
                    'focus_dist': 10,
                    'background': Color((0.0, 0.0, 0.0))
                    }

    cam = Camera(camera_param)
    cam.render(world, pool)


def main():
    num_processes = 8
    pool = Pool(processes=num_processes)
    switch = {1: random_spheres,
              2: two_sphere,
              3: earth,
              4: two_perlin_spheres,
              5: quads,
              6: simple_light}
    switch.get(6)(pool)

    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
