from pygame.math import Vector2

from kit.math import min_vector, max_vector, vector2tuple, DoubleLinkedList, DoubleLinkedNode
from kit.graphics import Color, random_color


def is_point_in_polygon(point: tuple[int, int], polygon: list[Vector2]):
    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


class Polygon:
    color: Color
    vertices: DoubleLinkedList[Vector2]
    filled_area: set[Vector2]

    def __init__(self, color: Color, vertices: list[Vector2]) -> None:
        self.color = color
        self.vertices = DoubleLinkedList[Vector2](vertices)
        self.filled_area = set([vector2tuple(vertex) for vertex in vertices])

        self.vertices_colors = [random_color() for _ in range(len(vertices))]

        self.fill()

    def fill(self) -> None:
        vertices = self.vertices.to_list()
        min_vertex = max_vertex = vertices[0]

        for vertex in vertices:
            min_vertex = min_vector(vertex, min_vertex)
            max_vertex = max_vector(vertex, max_vertex)

        min_x, min_y = int(min_vertex.x), int(min_vertex.y)

        width = int(max_vertex.x - min_x) - 1
        height = int(max_vertex.y - min_y) - 1

        for x in range(width):
            for y in range(height):
                point = min_x + x + 1, min_y + y + 1

                if is_point_in_polygon(point, vertices):
                    self.filled_area.add(point)

    def expand(self) -> None:
        directions = [ Vector2(0, -1), Vector2(1, 0), Vector2(0, 1), Vector2(-1, 0) ]

        for node in self.vertices:
            vertex = node.value

            for direction in directions:
                new_vertex = vertex + direction
                new_vertex_tuple = vector2tuple(new_vertex)

                if new_vertex_tuple in self.filled_area:
                    continue

                self.vertices.insert_before(new_vertex, node)
                self.filled_area.add(new_vertex_tuple)

        for node in self.vertices:
            vertex = node.value

            for direction in directions:
                new_vertex = vertex + direction
                new_vertex_tuple = vector2tuple(new_vertex)

                if new_vertex_tuple not in self.filled_area:
                    break
            else:
                self.vertices.remove_node(node)

        for node in self.vertices:
            self.check_distance(node)

        self.vertices_colors = [random_color() for _ in range(len(self.vertices.to_list()))]

    def check_distance(self, node: DoubleLinkedNode) -> None:
        node_a = node.after_node

        if node_a is None:
            return

        distance = node.value.distance_squared_to(node_a.value)

        if distance <= 2:
            return

        node_b = node_a.after_node

        if node_b is None:
            return
        
        print(node, node_a, node_b)
        
        self.vertices.flip_nodes(node_a, node_b)
