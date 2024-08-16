from typing import Optional

import numpy as np

from kit.pools import PoolLink, PoolFuture, PoolManager
from kit.graphics import Color

from .world import World
from .territory import Territory


class Player:
    id: int
    color: Color
    world: World
    territory: PoolLink

    _ticks: int
    _auto_expansion: Optional[int]
    _expansion_future: PoolFuture
    _expansion_cooldown: int

    def __init__(self, id: int, color: Color, world: World, manager: PoolManager) -> None:
        self.id = id
        self.color = color
        self.world = world
        self.territory_id = id + 1

        self.territory = manager.link(Territory, world.data, self.territory_id, _async=False)

        self._ticks = 0
        self._auto_expansion = 0
        self._expansion_future = None
        self._expansion_cooldown = 1

    def load_territory(self, points: np.matrix) -> None:
        points = np.clip(points, 0, [self.world.width - 1, self.world.height - 1])
        
        self.world.draw_points(self.color, points)
        self.territory.call_method("set_points", points, _async=False)

    def remove_territory(self) -> None:
        self.territory.delete()

    def _expansion_callback(self, future: PoolFuture) -> None:
        if future.result is None:
            self._auto_expansion = None

            return

        new_points, expansed = future.result

        if expansed:
            self.world.players[expansed].remove_territory()

        self.world.draw_points(self.color, new_points)

    def expanse(self, other_player: Optional["Player"] = None) -> None:
        self._auto_expansion = 0
        
        if other_player is not None:
            self._auto_expansion = other_player.territory_id

    def update(self) -> None:
        future = self._expansion_future

        if future is None or future.done:
            if self._auto_expansion is not None and self._ticks % self._expansion_cooldown == 0:
                self._expansion_future = self.territory.call_method("expanse", self._auto_expansion)
                self._expansion_future.add_callback(self._expansion_callback)
        
        self._ticks += 1
