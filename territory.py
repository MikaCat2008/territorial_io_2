import numpy as np

from kit.utils import in_pool, PoolObject


class Territory(PoolObject):
    points: set[tuple[int, int]]
    contour: set[tuple[int, int]]

    def __init__(self, id: int) -> None:
        super().__init__(id)

        self.points = set()
        self.contour = set()

    @in_pool
    def set_points(self, points: set[tuple[int, int]]) -> None:
        self.points |= points
        
        directions = [ (-1, 0), (0, 1), (1, 0), (0, -1) ]

        for x, y in self.points:
            contour = False

            for dx, dy in directions:
                point = x + dx, y + dy

                if point not in self.points:
                    contour = True

                    break
            
            if contour:
                self.contour.add((x, y))

    @in_pool
    def expanse(self) -> set[tuple[int, int]]:
        to_remove = set()
        new_points = set()
        directions = [ (-1, 0), (0, 1), (1, 0), (0, -1) ]

        for x, y in self.contour:
            for dx, dy in directions:
                point = x + dx, y + dy

                if point in self.points:
                    continue

                new_points.add(point)
            
            to_remove.add((x, y))
        
        self.contour -= to_remove
        self.contour |= new_points

        return np.array(list(new_points))