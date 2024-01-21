from .utils import Image


class Material:
    def __init__(self):
        self.texture: Image = Image()
        # self.color = (255, 255, 255)

        self.diffuse_intensity = 60
        self.specular_intensity = 1
        self.glossiness = 1