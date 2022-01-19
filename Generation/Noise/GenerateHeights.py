from . import Noise
import PIL.Image
from . import StandartNoise


def GenerateNoiseTex(
    seed=None,
    size=StandartNoise.SIZE,
    res=StandartNoise.RES,
    frameres=StandartNoise.FRAMES,
    space_range=StandartNoise.SPACW_RANGE,
    frame_range=StandartNoise.FRAME_RANGE,
):
    if seed:
        pnf = Noise.PerlinNoiseFactory(
            3, seed, octaves=4, tile=(space_range, space_range, frame_range)
        )
    else:
        pnf = Noise.PerlinNoiseFactory(
            3, octaves=4, tile=(space_range, space_range, frame_range)
        )
    img = PIL.Image.new("L", (size, 1))
    for x in range(size):

        n = pnf(x / res, 1 / res, 1 / frameres)
        img.putpixel((x, 0), int((n + 1) / 2 * 255 + 0.5))

    img.save("heightmap.png")
    return size
