from pygame import Vector3
from .entity import Entity


class Mesh(Entity):
    def __init__(self):
        super().__init__()
        self.meshes = []  # [(object name, Material name, vertices+uv data)]
        self.materials = {}  # Name: Material attributes
        self.animations = []

    def update(self, scene):
        super().update(scene)

        scene.active_camera.render(self, scene)