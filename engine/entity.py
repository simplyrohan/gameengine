from pygame import Vector3
from ._utils import EntityLike, SceneLike


class Entity:
    def __init__(self) -> None:
        # Heirachy
        self._parent: EntityLike = None
        self._children: list[Entity] = []

        # Transform
        self.position: Vector3 = Vector3()
        self.forward: Vector3 = Vector3(1, 0, 0)
        self.scale: Vector3 = Vector3(1, 1, 1)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value: EntityLike):
        self._parent = value
    
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
        for child in self.children:
            child.update(scene)
        