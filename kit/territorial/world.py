from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import numpy as np
from pygame.surface import Surface

from kit.pools import PoolLink, PoolEntity, PoolFuture, PoolManager
from kit.graphics import blit_points, Color, Camera

from .territory import Territory

if TYPE_CHECKING:
    from .player import Player


class WorldData(PoolEntity):
    width: int
    height: int
    points: np.matrix
    territories: dict[int, Territory]

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.points = np.zeros((width, height), dtype=np.uint8)
        self.territories = {}

    def get_point(self, point: tuple[int, int]) -> Optional[int]:
        x, y = point

        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return        

        return self.points[point]

    def get_contours(self) -> list[tuple[int, np.ndarray]]:
        return [
            (territory_id, territory.contour) 
            for territory_id, territory in self.territories.items()
            if len(territory.contour) > 0
        ]

    def add_territory(self, territory: Territory) -> None:
        self.territories[territory.territory_id] = territory

    def remove_territory(self, territory: Territory) -> None:
        del self.territories[territory.territory_id]


class World:
    width: int
    height: int
    surface: Surface
    players: dict[int, Player]
    contours: dict[int, np.ndarray]

    data: PoolLink
    manager: PoolManager

    _ticks: int
    _get_contours_future: Optional[PoolFuture]
    _get_contours_cooldown: int

    def __init__(self, width: int, height: int, players: dict[int, Player], manager: PoolManager) -> None:
        self.width = width
        self.height = height
        self.surface = Surface((width, height))
        self.players = players
        self.contours = {}

        self.data = manager.link(WorldData, width, height, _async=False)
        self.manager = manager

        self._ticks = 0
        self._get_contours_future = None
        self._get_contours_cooldown = 2

        for player in players:
            self.add_player(player)

    def get_point(self, point: tuple[int, int]) -> Optional[int]:
        return self.data.call_method("get_point", point, _async=False)

    def get_contours(self) -> list[tuple[int, np.ndarray]]:
        return self.data.call_method("get_contours")

    def add_player(self, player: Player) -> Player:        
        self.data.call_method("add_territory", player.territory)
        self.players[player.territory_id] = player

        return player

    def draw_points(self, color: Color, points: np.ndarray) -> None:
        blit_points(self.surface, color, points)

    def _get_contours_callback(self, future: PoolFuture) -> None:
        self.contours = future.result

        for territory_id, contour in self.contours:
            player = self.players[territory_id]
            player.contour = contour

    def draw(self, camera: Camera, selected_territory_id: int) -> None:        
        future = self._get_contours_future
        surface = self.surface.copy()

        if self._ticks % self._get_contours_cooldown == 0 and (future is None or future.done):
            self._get_contours_future = self.get_contours()
            self._get_contours_future.add_callback(self._get_contours_callback)

        if self.contours:
            for territory_id, contour in self.contours:
                if territory_id == selected_territory_id:
                    color = Color.BLACK
                else:
                    player = self.players[territory_id]
                    color = player.color - Color(20)

                blit_points(surface, color, contour)

        camera.blit(surface)

        self._ticks += 1
