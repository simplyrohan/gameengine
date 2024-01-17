from .entity import Entity
import pygame as _pg
from math import asin, atan2

class Camera(Entity):
    def __init__(self) -> None:
        super().__init__()
        self._pg = None
    
    def render(self, mesh, scene):
        if self._pg is None:
            self._pg = _pg.surfarray.pixels2d(_pg.display.get_surface())

        for name, material, data in mesh.meshes:
            material = mesh.materials[material]
            
            # Transform and project
            for vertex in data:
                pass