from PIL import Image

img = Image.open("heightmap.png")
rgb_im = img.convert('RGB')

for i in range(4000):
    print(rgb_im.getpixel((i, 0)))