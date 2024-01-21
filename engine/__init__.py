from .entity import Entity
from .scene import Scene
from .utils import Image
from .mesh import Mesh
import pygame as _pg


class App:
    def __init__(self, scene: Scene, dev=False):
        self.scene: Scene = scene

        self._pg = _pg.display.set_mode((800, 600))
        _pg.display.set_caption("Engine")
        self._pg_clock = _pg.time.Clock()

        self._title = "Engine"
        # Settings
        self.fps = 60

        self.dev = dev

    @property
    def title(self):
        return self._title
        

    @title.setter
    def title(self, value: str):
        self._title = value
        _pg.display.set_caption(value)

    @property
    def width(self):
        return _pg.display.get_surface().get_width()

    @width.setter
    def width(self, value: int):
        _pg.display.get_surface().set_width(value)

    @property
    def height(self):
        return _pg.display.get_surface().get_height()

    @height.setter
    def height(self, value: int):
        _pg.display.get_surface().set_height(value)

    @property
    def allow_screen_saver(self):
        return _pg.display.get_allow_screen_saver()

    @allow_screen_saver.setter
    def allow_screen_saver(self, value: bool):
        _pg.display.set_allow_screen_saver(value)

    @property
    def icon(self):
        return _pg.display.get_icon()

    @icon.setter
    def icon(self, value: Image):
        _pg.display.set_icon(value._pg)

    def run(self):
        dt = 0
        running = True
        while type(self.scene) == Scene and running:
            for event in _pg.event.get():
                if event.type == _pg.QUIT:
                    running = False
                    self.scene.exit()
            self.scene = self.scene.update(self._pg, delta=dt)
            dt = self._pg_clock.tick(self.fps)
            if self.dev:
                _pg.display.set_caption(
                    f"{self.title} | FPS: {self._pg_clock.get_fps():.2F}"
                )
            _pg.display.flip()
