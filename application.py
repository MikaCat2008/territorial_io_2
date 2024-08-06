import pygame as pg

pg.init()
pg.font.init()

from pygame import mouse
from pygame.font import SysFont
from pygame.math import Vector2
from pygame.draw import lines, circle
from pygame.display import set_mode, set_caption

from kit.game import Game
from kit.math import clamp
from kit.input import Keyboard
from kit.graphics import Color, random_color, scaled_lines, scaled_polygon

from polygon import Polygon
from serialization import create_save, open_save


def connect_points(pos_a: tuple[int, int], pos_b: tuple[int, int]) -> list[Vector2]:
    points = []

    x1, y1 = pos_a
    x2, y2 = pos_b
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    err = dx - dy

    while True:
        e2 = 2 * err

        if e2 > -dy:
            err -= dy
            x1 += sx

        if e2 < dx:
            err += dx
            y1 += sy

        if x1 == x2 and y1 == y2:
            break
        
        points.append(Vector2(x1, y1))

    return points


def check_points_connection(points: list[Vector2]) -> None:
    j = 0
    length = len(points)
    points_copy = points.copy()

    for i, point in enumerate(points_copy):
        next_point = points_copy[(i + 1) % length]

        distance = point.distance_squared_to(next_point)

        if distance > 2:
            connected_points = connect_points(point, next_point)
            points = points[:i + j + 1] + connected_points + points[i + j + 1:]

            j += len(connected_points)

    new_points = []

    for i, point in enumerate(points):
        if point in new_points:
            continue

        new_points.append(point)

    return new_points


class Application(Game):
    zoom: float
    offset: Vector2
    draw_contours: bool

    points: list[Vector2]
    polygons: list[Polygon]

    def __init__(self) -> None:
        super().__init__()

        self.zoom = 20
        self.screen = set_mode((1200, 600))
        self.offset = Vector2(0, 0)
        self.draw_contours = False

        self.points = []
        self.polygons = []

        self.font = SysFont(None, 24)

    def update(self) -> None:
        super().update()

        if mouse.get_pressed()[0]:
            point = Vector2(mouse.get_pos() - Vector2(self.screen.get_size()) / 2) / self.zoom - self.offset
            point //= 1

            if point not in self.points:
                self.points.append(point)
        if mouse.get_pressed()[2]:
            self.points = []

        move = 10 / self.zoom

        if Keyboard.get_pressed(pg.K_a):
            self.offset.x += move
        if Keyboard.get_pressed(pg.K_d):
            self.offset.x -= move
        if Keyboard.get_pressed(pg.K_w):
            self.offset.y += move
        if Keyboard.get_pressed(pg.K_s):
            self.offset.y -= move

        if Keyboard.get_pressed(pg.K_MINUS):
            self.zoom *= 0.95
        if Keyboard.get_pressed(pg.K_EQUALS):
            self.zoom *= 1.05

        self.zoom = clamp(self.zoom, 0.25, 256)

        if Keyboard.get_clicked(pg.K_v):
            points = check_points_connection(self.points)

            self.polygons.append(Polygon(random_color(50, 205), points))
            self.points = []

        if Keyboard.get_clicked(pg.K_c):
            create_save(self.polygons)
        if Keyboard.get_clicked(pg.K_x):
            self.polygons = open_save()
        
        if Keyboard.get_clicked(pg.K_e):
            self.polygons[0].expand()
        if Keyboard.get_pressed(pg.K_r):
            self.polygons[0].expand()
        if Keyboard.get_clicked(pg.K_p):
            self.draw_contours = not self.draw_contours

    def draw(self) -> None:
        camera_offset = self.offset + Vector2(self.screen.get_size()) / self.zoom / 2
        
        for polygon in self.polygons:
            vertices = polygon.vertices.to_list()
            
            scaled_polygon(
                self.screen,
                self.zoom,
                polygon.color,
                camera_offset,
                vertices
            )
            scaled_lines(
                self.screen,
                self.zoom,
                polygon.color - Color(20),
                camera_offset,
                vertices
            )

            if self.draw_contours:
                _vertices = [
                    self.zoom * (vertex + Vector2(0.5) + self.offset) + Vector2(self.screen.get_size()) / 2
                    for vertex in vertices
                ]

                for i, vertex_a in enumerate(_vertices):
                    vertex_b = _vertices[(i + 1) % len(vertices)]

                    lines(self.screen, polygon.vertices_colors[i], False, [vertex_a, vertex_b])
                    circle(self.screen, (255, 255, 255), vertex_a, self.zoom / 10)
                    text = self.font.render(str(i), False, (0, 0, 0))
                    self.screen.blit(text, vertex_a - Vector2(text.get_size()) / 2)

        if len(self.points) > 1:
            scaled_lines(
                self.screen, 
                self.zoom, 
                (255, 255, 255), 
                camera_offset,
                self.points
            )

        set_caption(f"{self.clock.get_fps():.2f} fps | {self.zoom:.2f} zoom")

        super().draw()
