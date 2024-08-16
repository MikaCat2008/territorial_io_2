from typing import ClassVar, Optional

from pygame.rect import Rect
from pygame.math import Vector2
from pygame.surface import Surface
from pygame.transform import scale_by

from kit.math import clip, min_vector, max_vector, round_vector
from kit.input import Mouse

from .color import (
    Color as Color, 
    random_color as random_color
)


class Camera:
    zoom: float
    screen: Surface
    position: Vector2

    min_zoom: ClassVar[float] = 0.02
    max_zoom: ClassVar[float] = 256
    zooming_speed: ClassVar[float] = 1.15

    def __init__(self, screen: Surface, zoom: float, position: Vector2) -> None:
        self.zoom = zoom
        self.screen = screen
        self.position = position

    def zoom_in(self) -> None:
        self.zoom = clip(self.zoom * self.zooming_speed, self.min_zoom, self.max_zoom)

    def zoom_out(self) -> None:
        self.zoom = clip(self.zoom / self.zooming_speed, self.min_zoom, self.max_zoom)

    def get_mouse_pos(self) -> Vector2:
        mouse_pos = Vector2(Mouse.get_pos())
        mouse_pos -= Vector2(self.screen.get_size()) / 2
        mouse_pos /= self.zoom
        mouse_pos += self.position

        return mouse_pos

    def blit(self, surface: Surface, rect: Optional[Rect] = None) -> None:
        offset = self.position.copy()

        screen_size = Vector2(self.screen.get_size())
        unscaled_screen_size = screen_size / self.zoom

        offset -= screen_size / 2 / self.zoom

        if rect is None:
            topleft = Vector2()
            bottomright = Vector2(surface.get_size())
        else:
            topleft = Vector2(rect.topleft)
            bottomright = Vector2(rect.bottomright)

        min_pos = max_vector(topleft, round_vector(offset)) - Vector2(1)
        max_pos = min_vector(bottomright, round_vector(unscaled_screen_size + offset)) + Vector2(2)

        size = max_pos.x - min_pos.x, max_pos.y - min_pos.y

        if size[0] < 1 or size[1] < 1:
            return
        
        _surface = Surface(size)
        _surface.blit(surface, topleft - min_pos)

        _surface = scale_by(_surface, (self.zoom, self.zoom))

        self.screen.blit(
            _surface, min_pos * self.zoom - offset * self.zoom
        )
