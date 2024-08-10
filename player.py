from typing import Optional
from threading import Thread

import numpy as np
from pygame.math import Vector2
from pygame.surface import Surface

from kit.utils import in_thread
from kit.graphics import Color, AutoSurface

from territory import Territory


class Player:
    surface: AutoSurface
    territory: Territory

    _ticks: int
    _expansion_thread: Optional[Thread]

    def __init__(self) -> None:
        self.surface = AutoSurface()
        self.territory = Territory.link()

        self._ticks = 0
        self._expansion_thread = None

    def load_points(self, points: set[tuple[int, int]]) -> None:
        self.territory.set_points(points)
        self.surface.set_points(np.array(list(points)), Color.WHITE)

    @in_thread
    def expanse_territory(self) -> None:
        points = self.territory.expanse()

        self.surface.set_points(points, Color.WHITE)

    def update(self) -> None:
        if self._ticks % 5 == 0:
            if self._ticks > 100:
                return
            
            thread = self._expansion_thread

            if thread is None or not thread.is_alive():
                self._expansion_thread = self.expanse_territory()

        self._ticks += 1

    def draw(self, screen: Surface, zoom: float, offset: Vector2) -> None:
        self.surface.blit(screen, zoom, offset.x, offset.y)
