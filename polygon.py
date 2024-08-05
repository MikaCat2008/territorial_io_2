from pygame.math import Vector2

from kit.math import vector2tuple, DoubleLinkedList
from kit.graphics import Color


class Polygon:
    color: Color
    vertices: DoubleLinkedList[Vector2]
    filled_area: set[Vector2]

    def __init__(
        self, 
        color: Color, 
        vertices: list[Vector2], 
        filled_area: set[tuple[float, float]] = None
    ) -> None:
        self.color = color
        self.vertices = DoubleLinkedList[Vector2](vertices)
        self.filled_area = set(map(vector2tuple, vertices)) | (filled_area or set())

    def expand(self) -> None:
        for node in self.vertices:
            vertex = node.value

            for direction in [ Vector2(0, -1), Vector2(1, 0), Vector2(0, 1), Vector2(-1, 0) ]:
                new_vertex = vertex + direction
                new_vertex_tuple = vector2tuple(new_vertex)

                if new_vertex_tuple in self.filled_area:
                    continue

                self.vertices.insert_before(new_vertex, node)
                self.filled_area.add(new_vertex_tuple)

            self.vertices.remove_node(node)
