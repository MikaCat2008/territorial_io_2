from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import numpy as np

from kit.pools import PoolEntity

if TYPE_CHECKING:
    from .world import WorldData

directions = np.array([(-1, 0), (0, 1), (1, 0), (0, -1)])
extended_directions = directions[None, :, :]


class Territory(PoolEntity):
    world: WorldData
    contour: Optional[np.ndarray]
    territory_id: int

    def __init__(self, world: WorldData, territory_id: int) -> None:
        self.world = world
        self.contour = None
        self.territory_id = territory_id

    def set_points(self, points: np.ndarray) -> None:
        self.world.points[points[:, 0], points[:, 1]] = self.territory_id

        neighbours = np.clip(points[:, None, :] + extended_directions, 0, [self.world.width - 1, self.world.height - 1])
        contour_mask = np.any(
            self.world.points[neighbours[:, :, 0], neighbours[:, :, 1]] != self.territory_id, 
            axis=1
        )
        contour_points = points[contour_mask]

        if self.contour is None:
            self.contour = contour_points
        else:
            self.contour = np.vstack(self.contour, contour_points)

    def expanse(self, expanse_id: int) -> Optional[tuple[np.ndarray, bool]]:
        if len(self.contour) == 0:
            return

        if expanse_id:
            other_territory = self.world.territories.get(expanse_id)

            if other_territory is None:
                return
            
        extended_contour = self.contour[:, None, :] + extended_directions
        extended_contour = np.clip(
            extended_contour, 0, [self.world.width - 1, self.world.height - 1]
        )

        new_points_mask = self.world.points[extended_contour[:, :, 0], extended_contour[:, :, 1]] == expanse_id
        new_points = extended_contour[new_points_mask]

        if len(new_points) == 0:
            return
        
        self.world.points[new_points[:, 0], new_points[:, 1]] = self.territory_id

        if expanse_id > 0:
            other_extended_points = np.concatenate(
                new_points[:, None, :] + extended_directions
            )
            other_extended_points = np.clip(
                other_extended_points, 0, [self.world.width - 1, self.world.height - 1]
            )

            other_new_points_mask = self.world.points[
                other_extended_points[:, 0], other_extended_points[:, 1]
            ] == expanse_id
            other_new_points = other_extended_points[other_new_points_mask]

            other_contour_set = set(map(tuple, other_territory.contour.tolist()))
            other_contour_set |= set(map(tuple, other_new_points.tolist()))
            other_contour_set -= set(map(tuple, new_points.tolist()))

            other_territory.contour = np.array(list(other_contour_set))

        remove_mask = np.all(
            self.world.points[extended_contour[:, :, 0], extended_contour[:, :, 1]] == self.territory_id, 
            axis=1
        )
        remove_points = self.contour[remove_mask]

        contour_set = set(map(tuple, self.contour.tolist()))
        contour_set |= set(map(tuple, new_points.tolist()))
        contour_set -= set(map(tuple, remove_points.tolist()))

        self.contour = np.array(list(contour_set))

        if expanse_id and len(other_contour_set) == 0:
            return new_points, expanse_id
        else:
            return new_points, 0

    def delete(self) -> None:
        self.world.remove_territory(self)
