from .utils import Image


class Material:
    def __init__(self):
        self.texture: Image = Image()
        # self.color = (255, 255, 255)

        self.diffuse_intensity = 60
        self.specular_intensity = 1
        self.glossiness = 1
    
    @property
    def albedo(self):
        return self.texture._pg.get_at((0, 0))
    
    @albedo.setter
    def albedo(self, value):
        self.texture._pg.fill(value)