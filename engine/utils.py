import pygame


class Image:
    def __init__(self, path: str = None):
        if path is None:
            self._pg = pygame.Surface((1, 1))
            self._pg.fill((120, 120, 120))
        else:
            self._pg = pygame.image.load(path)


Color = pygame.Color
