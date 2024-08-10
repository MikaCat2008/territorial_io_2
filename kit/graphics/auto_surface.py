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

    def blit(self, screen: Surface, scale=1, offset_x=0, offset_y=0) -> None:
        if self._rect is None or self._surface is None:
            return

        screen_size = Vector2(screen.get_size())
        unscaled_screen_size = screen_size / scale

        offset_x -= unscaled_screen_size.x / 2
        offset_y -= unscaled_screen_size.y / 2

        min_x, min_y = Vector2(self._rect.topleft)
        max_x, max_y = Vector2(self._rect.bottomright)

        min_x = max(min_x, offset_x // 1) - 1
        min_y = max(min_y, offset_y // 1) - 1

        max_x = min(max_x, unscaled_screen_size.x // 1 + offset_x // 1) + 2
        max_y = min(max_y, unscaled_screen_size.y // 1 + offset_y // 1) + 2

        size = max_x - min_x, max_y - min_y

        if size[0] < 1 or size[1] < 1:
            return
        
        surface = Surface(size)
        surface.set_colorkey((0, 0, 0))
        surface.blit(
            self._surface.copy(), 
            (self._rect.left - min_x, self._rect.top - min_y)
        )

        surface = scale_by(surface, (scale, scale))
        surface.set_colorkey((0, 0, 0))

        screen.blit(
            surface, (
                min_x * scale - offset_x * scale, 
                min_y * scale - offset_y * scale
            )
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
