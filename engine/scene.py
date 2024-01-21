from .entity import Entity
from ._utils import EntityLike, SceneLike
import pygame as _pg
from .camera import Camera
from .utils import Color
from .shader import Shader


class Scene:
    def __init__(self):
        self._children: list[EntityLike] = []
        
        self.active_camera = Camera()
        self.add(self.active_camera)

        self.ambient_background: Color = Color(30, 30, 32)

        self.deltatime: float = 0

        self._frame_tasks = []

        self.shader = Shader(lambda x, y, z, normal, color, material, scene: color)

    def update(self, screen: _pg.Surface, delta: float):
        self.deltatime = delta
        screen.fill(self.ambient_background)
        for child in self.children:
            child.update(self)

        # Draw all children
        for task in self._frame_tasks:
            task(self.deltatime)

        return self

    @property
    def children(self):
        return self._children

    def add(self, child: EntityLike):
        self._children.append(child)
        child.parent = self


    def exit(self):
        for child in self.children:
            child.exit()

    @property
    def true_pos(self):
        return _pg.Vector3(0, 0, 0)

    @property
    def true_rot(self):
        return _pg.Vector3(0, 0, 0)
    