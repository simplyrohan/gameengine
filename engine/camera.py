from .entity import Entity
import pygame as _pg
from math import asin, atan2


def bary_to_cart(bary, triangle):
    return [
        bary[0] * triangle[0][0] + bary[1] * triangle[1][0] + bary[2] * triangle[2][0],
        bary[0] * triangle[0][1] + bary[1] * triangle[1][1] + bary[2] * triangle[2][1],
    ]


def cart_to_bary(cart: tuple[int, int], triangle: list[tuple, tuple, tuple]):
    # Bartriangle[2][1] = 1 - bartriangle[0][1] - bartriangle[1][1]
    # Bartriangle[1][1] = bary[3] - bartriangle[0][1] + 1
    # Bartriangle[0][1] = bartriangle[2][1] - bar[1] + 1
    y2y3 = triangle[1][1] - triangle[2][1]
    x3x2 = triangle[2][0] - triangle[1][0]
    xx2 = cart[0] - triangle[2][0]
    yy2 = cart[1] - triangle[2][1]
    x0x2 = triangle[0][0] - triangle[2][0]
    denominator = y2y3 * x0x2 + x3x2 * (triangle[0][1] - triangle[2][1])

    if denominator == 0:
        return (-1, -1, -1)

    b1 = (y2y3 * xx2 + x3x2 * yy2) / denominator

    b2 = ((triangle[2][1] - triangle[0][1]) * xx2 + x0x2 * yy2) / denominator

    return [b1, b2, 1 - b1 - b2]


class Camera(Entity):
    def __init__(self) -> None:
        super().__init__()
        self._pg = None

    def render(self, mesh, scene):
        focal = (90, 90)
        if self._pg is None:
            self._pg = _pg.display.get_surface()
        buffer = [
            [float("inf") for _ in range(self._pg.get_width())]
            for _ in range(self._pg.get_height())
        ]

        for name, material, data in mesh.meshes:
            material = mesh.materials[material]

            # Transform and project
            for face in data:
                zs = []
                projected_face = []
                uvs = []
                for vertex, uv in face:
                    # Transform
                    vertex = vertex.rotate_x(mesh.true_rot.x)
                    vertex = vertex.rotate_y(mesh.true_rot.y)
                    vertex = vertex.rotate_z(mesh.true_rot.z)
                    vertex = vertex * mesh.scale
                    vertex = vertex + mesh.true_pos

                    projected = _pg.Vector2(
                        int((vertex.x * focal[0]) / (focal[0] + vertex.z)),
                        int((vertex.y * focal[1]) / (focal[1] + vertex.z)),
                    )
                    projected_face.append(
                        projected
                        + (self._pg.get_width() / 2, self._pg.get_height() / 2)
                    )
                    zs.append(vertex.z)
                    uvs.append(uv)
                # Draw bary
                txs, tys = zip(*projected_face)
                rz = min(zs)
                uvs = [
                    (uv[0] / (z / rz), (uv[1]) / (z / rz)) for uv, z in zip(uvs, zs)
                ]  # uvs and zs
                zs = [(1 / z) for z in zs]

                tx, ty = int(min(txs)), int(min(tys))
                tw, th = int(max(txs) - tx), int(max(tys) - ty)

                for x in range(tw):
                    for y in range(th):
                        # Part of triangle
                        bary = cart_to_bary((tx + x, ty + y), projected_face)
                        if bary[0] < 0 or bary[1] < 0 or bary[2] < 0:
                            continue

                        z = 1 / (bary[0] * zs[0] + bary[1] * zs[1] + bary[2] * zs[2])
                        if buffer[tx + x][ty + y] > z:
                            buffer[tx + x][ty + y] = z
                            uv = bary_to_cart(bary, uvs)
                            uv[0] = (uv[0] * (z / rz)) % 1
                            # print(uv)
                            uv[1] = (uv[1] * (z / rz)) % 1
                            uv = (
                                uv[0] * (material.texture._pg.get_width() - 1),
                                uv[1] * (material.texture._pg.get_height() - 1),
                            )

                            color = material.texture._pg.get_at(uv)
                            self._pg.set_at((tx + x, ty + y), color)

    # _pg.draw.polygon(self._pg, material.color, projected_face)
