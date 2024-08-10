from typing import Optional

import numpy as np

import pygame as pg
from pygame.rect import Rect
from pygame.draw import lines
from pygame.math import Vector2
from pygame.surface import Surface
from pygame.surfarray import pixels3d
from pygame.transform import scale_by

from .color import Color


class AutoSurface:
    _rect: Optional[Rect]
    _surface: Optional[Surface]

    def __init__(self) -> None:
        self._rect = None
        self._surface = None

    def blit(self, screen: Surface, scale: float = 1) -> None:
        if self._rect is None or self._surface is None:
            return

        screen_w, screen_h = screen.get_size()
        screen_w, screen_h = screen_w // scale, screen_h // scale
        
        min_x, min_y = self._rect.topleft
        max_x, max_y = self._rect.bottomright

        min_x = max(min_x, 0)
        min_y = max(min_y, 0)

        max_x = min(max_x, screen_w)
        max_y = min(max_y, screen_h)

        surface = Surface((max_x - min_x + 1, max_y - min_y + 1))
        surface.set_colorkey((0, 0, 0))
        surface.blit(self._surface.copy(), (self._rect.left - min_x, self._rect.top - min_y))

        screen.blit(
            scale_by(surface, (scale, scale)), 
            (min_x * scale, min_y * scale)
        )

    def expand_rect(self, x: int, y: int, rect: Optional[Rect]) -> Rect:
        if rect is None:
            return Rect(x, y, 1, 1)

        rect = rect.copy()

        if x < rect.left:
            rect.width += rect.left - x
            rect.left = x
        if y < rect.top:
            rect.height += rect.top - y
            rect.top = y

        if x >= rect.right:
            rect.width += x - rect.right + 1
        if y >= rect.bottom:
            rect.height += y - rect.bottom + 1

        return rect

    def update(self, rect: Rect) -> None:
        if rect == self._rect:
            return
        
        new_surface = Surface(rect.size)
        new_surface.set_colorkey((0, 0, 0))

        if not (self._rect is None or self._surface is None):
            dest = self._rect.left - rect.left, self._rect.top - rect.top
            new_surface.blit(self._surface.copy(), dest)
            
        self._rect = rect
        self._surface = new_surface

    def set_points(self, points: np.matrix, color: Color) -> None:
        min_point = np.min(points, axis=0)
        max_point = np.max(points, axis=0)

        rect = self.expand_rect(*min_point, self._rect)
        rect = self.expand_rect(*max_point, rect)

        self.update(rect)

        pixel_array = pixels3d(self._surface)
        pixel_array[points[:, 0] - self._rect.left, points[:, 1] - self._rect.top] = color
        del pixel_array

    def remove_points(self, points: set[tuple[int, int]]) -> None:
        for x, y in points:
            point = x - self._rect.left, y - self._rect.top
            
            self._surface.set_at(point, (0, 0, 0, 0))

        rect = self._surface.get_bounding_rect()

        self.update(rect.move(self._rect.topleft))
