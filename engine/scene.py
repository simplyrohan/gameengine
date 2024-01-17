from .entity import Entity
from ._utils import EntityLike, SceneLike
import pygame as _pg
from .camera import Camera
from .utils import Color


class Scene:
    def __init__(self):
        self._children: list[EntityLike] = []
        
        self.active_camera = Camera()

        self.ambient_background: Color = Color(30, 30, 32)

        self.deltatime: float = 0

    def update(self, screen: _pg.Surface, delta: float):
        self.deltatime = delta
        screen.fill(self.ambient_background)
        for child in self.children:
            child.update(self)

        # Draw all children

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
