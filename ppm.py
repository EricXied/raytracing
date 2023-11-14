from PIL import Image

image_width = 256
image_height = 256
backgroud = 0

data = [backgroud] * image_height * image_width

for i in range(image_height):
    for j in range(image_width):
        data[i + j * image_width] = (i,j,0)
im = Image.new("RGB", (image_width,image_height))
im.putdata(data)
im.save('test.png')
