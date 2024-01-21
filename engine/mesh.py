from pygame import Vector3, Vector2
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
        uvs = []
        normals = []
        meshes = [[]]
        for line in lines:
            line = line.strip()
            if line.startswith("v "):
                vertices.append(Vector3(*map(float, line[2:].split(" "))))
            elif line.startswith("vt "):
                uvs.append(Vector2(*map(float, line[3:].split(" ")[:2])))
            elif line.startswith("vn "):
                normals.append(Vector3(*map(float, line[3:].split(" "))))
            if line.startswith("f "):
                if len(line[2:].split(" ")[0].split("/")) == 3:
                    
                    meshes[-1].append(
                        [
                            (
                                vertices[int(i.split("/")[0]) - 1],
                                uvs[int(i.split("/")[1]) - 1],
                                normals[int(i.split("/")[2]) - 1],
                            )
                            for i in line[2:].split(" ")
                        ]
                    )
                elif len(line[2:].split(" ")[0].split("/")) == 2:
                    meshes[-1].append(
                        [
                            (
                                vertices[int(i.split("/")[0]) - 1],
                                uvs[int(i.split("/")[1]) - 1],
                            )
                            for i in line[2:].split(" ")
                        ]
                    )
                else:
                    meshes[-1].append(
                        [(vertices[int(i.split("/")[0]) - 1], (0, 0), (0, 0, 0)) for i in line[2:].split(" ")]
                    )

        mesh = Mesh()
        mesh.meshes = [
            [
                "default",
                "default",  # Name, Material
                [face for face in m],  # Vertices
            ]
            for m in meshes
        ]

        return mesh

    def update(self, scene):
        super().update(scene)

        scene.active_camera.render(self, scene)
