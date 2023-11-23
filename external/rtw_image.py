import os
from PIL import Image


class RtwImage:

    def __init__(self, image_filename, imagedir=None):
        self.filename = image_filename
        self.dir = imagedir
        self.bytes_per_pixel = 3
        self.path = self.find_path()
        if self.path:
            self.data = Image.open(self.path)
            self.img_width, self.img_height = self.data.size
            # self.data = self.data.convert("RGB")
            self.bytes_per_scanline = self.bytes_per_pixel * self.img_width

    def find_path(self):
        paths_to_try = []
        if self.dir:
            paths_to_try.append(os.path.join(self.dir, self.filename))
        paths_to_try.extend([
            self.filename,
            os.path.join('images', self.filename),
            os.path.join('..', 'images', self.filename),
            os.path.join('..', '..', 'images', self.filename),
            os.path.join('..', '..', '..', 'images', self.filename),
            os.path.join('..', '..', '..', '..', 'images', self.filename),
            os.path.join('..', '..', '..', '..', '..', 'images', self.filename),
            os.path.join('..', '..', '..', '..', '..', '..', 'images', self.filename),
            os.path.join('..', '..', '..', '..', '..', '..', '..', 'images', self.filename),
        ])
        for path in paths_to_try:
            if os.path.exists(path):
                return path
        return None

    def load(self):
        n = self.bytes_per_pixel
        image = Image.open(self.path)
        image_width, image_height = image.size
        bytes_per_scanline = image_width * n
        return image_width, image_height, bytes_per_scanline

    def pixel_data(self, x, y):
        if not self.path:
            return [255, 0, 255]
        x = self.clamp(x, 0, self.img_width)
        y = self.clamp(y, 0, self.img_height)

        return self.data.getpixel((x, y))

    def clamp(self, x, low, high):
        if x < low: return low
        if x < high: return x
        return high - 1

    def width(self):
        return self.img_width if self.path else 0

    def height(self):
        return self.img_height if self.path else 0


