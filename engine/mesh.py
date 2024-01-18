from pygame import Vector3
from .material import Material
from .entity import Entity


class Mesh(Entity):
    def __init__(self):
        super().__init__()
        self.meshes = []  # [(object name, Material name, vertices+uv data)]
        self.materials = {"default": Material()}  # Name: Material attributes
        self.animations = []

    def load_obj(path):
        with open(path, "r") as file:
            lines = file.readlines()
        vertices = []
        meshes = [[]]
        for line in lines:
            if line.startswith("v "):
                vertices.append(Vector3(*map(float, line[2:].split(" "))))
            if line.startswith("f "):
                meshes[-1].append([vertices[int(i.split("/")[0])-1] for i in line[2:].split(" ")])
        
        mesh = Mesh()
        mesh.meshes = [
            [
                "default",
                "default",  # Name, Material
                [
                    (
                        face,  # Vertices
                        [],  # UV
                    )
                    for face in m
                ],
            ] for m in meshes
        ]

        return mesh

    def update(self, scene):
        super().update(scene)

        scene.active_camera.render(self, scene)
