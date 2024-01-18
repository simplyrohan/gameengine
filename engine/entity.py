from pygame import Vector3
from ._utils import EntityLike, SceneLike


class Entity:
    def __init__(self) -> None:
        # Heirachy
        self.parent: EntityLike = None
        self._children: list[Entity] = []

        # Transform
        self.position: Vector3 = Vector3()
        self.rotation = Vector3(0, 0, 0)
        self.scale: float = 1

        self._frame_task = lambda scene: None

    @property
    def children(self):
        return self._children # Read-only

    @property
    def true_pos(self):
        return self.position + self.parent.true_pos # Read only

    @property
    def true_rot(self):
        return self.rotation + self.parent.true_rot # Read only


    def update(self, scene: SceneLike):
        self._frame_task(scene)
        for child in self.children:
            child.update(scene)
    
    def on_frame(self, wrapper):
        self._frame_task = wrapper