from pygame.math import Vector2

from .converter import (
    tuple2vector as tuple2vector,
    vector2tuple as vector2tuple
)
from .double_linked_list import (
    DoubleLinkedList as DoubleLinkedList
)


def clamp(value: float, min_value: float, max_value: float) -> float:
    if value > max_value:
        return max_value
    
    if value < min_value:
        return min_value
    
    return value


def max_vector(vector_a: Vector2, vector_b: Vector2) -> float:    
    return Vector2(max(vector_a.x, vector_b.x), max(vector_a.y, vector_b.y))


def get_vertices_bounds(vertices: list[Vector2]) -> tuple[Vector2, Vector2]:
    min_vertex = None
    max_vertex = None
    
    for vertex in vertices:
        if min_vertex is None:
            min_vertex = vertex.copy()
            max_vertex = vertex.copy()
        else:
            min_vertex.x = min(vertex.x, min_vertex.x)
            max_vertex.x = max(vertex.x, max_vertex.x)
            min_vertex.y = min(vertex.y, min_vertex.y)
            max_vertex.y = max(vertex.y, max_vertex.y)

    return min_vertex, max_vertex
