import pygame as pg
from pygame import mouse
from pygame.draw import lines
from pygame.math import Vector2
from pygame.display import set_mode, set_caption

from kit.game import Game
from kit.math import clamp
from kit.input import Keyboard
from kit.graphics import Color, random_color, scaled_lines, scaled_polygon

from polygon import Polygon
from serialization import create_save, open_save


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

    def update(self) -> None:
        super().update()

        if mouse.get_pressed()[0]:
            point = Vector2(mouse.get_pos() - Vector2(self.screen.get_size()) / 2) / self.zoom - self.offset

            if point not in self.points:
                self.points.append(point // 1)
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
            self.polygons.append(Polygon(random_color(50, 205), self.points))
            self.points = []

        if Keyboard.get_clicked(pg.K_c):
            create_save(self.polygons)
        if Keyboard.get_clicked(pg.K_x):
            self.polygons = open_save()
        
        if Keyboard.get_clicked(pg.K_e):
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
                lines(self.screen, (255, 255, 255), False, [
                    self.zoom * (vertex + Vector2(0.5) + self.offset) + Vector2(self.screen.get_size()) / 2
                    for vertex in vertices
                ])

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
