from typing import Optional

import numpy as np
from pygame.rect import Rect
from pygame.font import SysFont
from pygame.math import Vector2
from pygame.surface import Surface

from kit.pools import PoolLink, PoolFuture, PoolManager
from kit.graphics import Color, Camera

from .world import World
from .territory import Territory


class Player:
    id: int
    name: str
    color: Color
    world: World

    in_game: bool
    contour: Optional[np.ndarray]
    territory_id: int

    territory: PoolLink
    name_texture: Surface

    _ticks: int
    _auto_expansion: Optional[int]
    _expansion_future: PoolFuture
    _expansion_cooldown: int

    def __init__(self, id: int, name: str, color: Color, world: World, manager: PoolManager) -> None:
        self.id = id
        self.name = name
        self.color = color
        self.world = world

        self.in_game = True
        self.contour = None
        self.territory_id = id + 1

        font = SysFont(None, 22)

        self.territory = manager.link(Territory, world.data, self.territory_id, _async=False)
        self.name_texture = font.render(name, None, Color.BLACK)

        self._ticks = 0
        self._auto_expansion = 0
        self._expansion_future = None
        self._expansion_cooldown = 1

    def load_territory(self, points: np.matrix) -> None:
        points = np.clip(points, 0, [self.world.width - 1, self.world.height - 1])
        
        self.world.draw_points(self.color, points)
        self.territory.call_method("set_points", points, _async=False)

    def remove_territory(self) -> None:
        self.in_game = False
        self.territory.delete()

    def _expansion_callback(self, future: PoolFuture) -> None:
        if future.result is None:
            self._auto_expansion = None

            return

        new_points, expanse_id, expansed = future.result

        if expansed:
            other_player = self.world.players[expanse_id]
            other_player.remove_territory()

        self.world.draw_points(self.color, new_points)

    def expanse(self, other_player: Optional["Player"] = None) -> None:
        self._auto_expansion = 0
        
        if other_player is not None:
            self._auto_expansion = other_player.territory_id

    def update(self) -> None:
        future = self._expansion_future

        if self.in_game and (future is None or future.done):
            if self._auto_expansion is not None and self._ticks % self._expansion_cooldown == 0:
                self._expansion_future = self.territory.call_method("expanse", self._auto_expansion)
                self._expansion_future.add_callback(self._expansion_callback)
        
        self._ticks += 1

    def draw(self, camera: Camera) -> None:
        if not self.in_game:
            return

        min_pos = np.min(self.contour, axis=0)
        max_pos = np.max(self.contour, axis=0)

        if min_pos is None:
            return
    
        pos = min_pos + (max_pos - min_pos) / 2 
        pos -= Vector2(self.name_texture.get_size()) / 2

        camera.blit(self.name_texture, Rect(pos, Vector2()), scale=False)
