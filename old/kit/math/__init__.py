from pygame.math import Vector2

from .converter import (
    tuple2vector as tuple2vector,
    vector2tuple as vector2tuple
)
from .double_linked_list import (
    DoubleLinkedList as DoubleLinkedList,
    DoubleLinkedNode as DoubleLinkedNode
)


def clamp(value: float, min_value: float, max_value: float) -> float:
    if value > max_value:
        return max_value
    
    if value < min_value:
        return min_value
    
    return value


def min_vector(vector_a: Vector2, vector_b: Vector2) -> float:    
    return Vector2(min(vector_a.x, vector_b.x), min(vector_a.y, vector_b.y))


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


def calculate_line_points(pos_a: tuple[int, int], pos_b: tuple[int, int]) -> set[tuple[int, int]]:
    x1, y1 = pos_a
    x2, y2 = pos_b

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    err = dx - dy
    points = set()

    while True:
        points.add((x1, y1))

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * err

        if e2 > -dy:
            err -= dy
            x1 += sx

        if e2 < dx:
            err += dx
            y1 += sy

    return points
