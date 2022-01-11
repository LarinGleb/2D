from Noise import PerlinNoiseFactory
import PIL.Image

size = 40000
res = 2
frames = 40
frameres = 10
space_range = size//res
frame_range = frames//frameres

pnf = PerlinNoiseFactory(3, octaves=4, tile=(space_range, space_range, frame_range))


img = PIL.Image.new('L', (size, 1))
for x in range(size):
    
    n = pnf(x/res, 1/res, 1/frameres)
    img.putpixel((x, 0), int((n + 1) / 2 * 255 + 0.5))

img.save("heightmap.png")

