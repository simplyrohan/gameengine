from .entity import Entity
import pygame as _pg
from math import asin, atan2


class Camera(Entity):
    def __init__(self) -> None:
        super().__init__()
        self._pg = None

    def render(self, mesh, scene):
        focal = (90, 90)
        if self._pg is None:
            self._pg = _pg.display.get_surface()

        for name, material, data in mesh.meshes:
            material = mesh.materials[material]

            # Transform and project
            for face, uvs in data:
                projected_face = []
                for vertex in face:
                    # Transform
                    vertex = vertex.rotate_x(mesh.true_rot.x)
                    vertex = vertex.rotate_y(mesh.true_rot.y)
                    vertex = vertex.rotate_z(mesh.true_rot.z)
                    vertex = vertex * mesh.scale
                    vertex = vertex + mesh.true_pos
                    projected = _pg.Vector2(
                        (vertex.x * focal[0]) / (focal[0] + vertex.z),
                        (vertex.y * focal[1]) / (focal[1] + vertex.z),
                    )
                    projected_face.append(
                        projected
                        + (self._pg.get_width() / 2, self._pg.get_height() / 2)
                    )
                _pg.draw.polygon(self._pg, material.color, projected_face)
