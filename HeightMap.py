from PIL import Image
from Generation import Noise

class HeightMap():
    def __init__(self):
        self.img = None
        self.size = 0

    def Generate(self):
        self.size = Noise.GenerateHeights.GenerateNoiseTex()
        self.img = Image.open("heightmap.png")

    def GetPixel(self, coord):
        
        return self.img.getpixel((self.size // 2 + coord, 0))