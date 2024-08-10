import pygame as pg
from pygame.math import Vector2
from pygame.display import set_mode, set_caption

pg.init()
pg.font.init()

from kit.game import Game
from kit.math import clamp
from kit.input import Keyboard
from kit.utils import PoolObject

from player import Player


class Application(Game):
    players: list[Player]
    camera_zoom: float
    camera_position: Vector2

    def __init__(self) -> None:
        super().__init__()

        PoolObject.create_pool()

        self.screen = set_mode((1200, 600))
        self.camera_zoom = 20
        self.camera_position = Vector2()

        self.players = [ Player(), Player() ]
        self.players[0].load_points({
            (-24, -25), (-25, -24), (-25, -25), (-25, -26), (-26, -25)    
        })
        self.players[1].load_points({
            (24, 25), (25, 24), (25, 25), (25, 26), (26, 25)    
        })

        Keyboard()

    def update(self) -> None:
        super().update()

        velocity = 10 / self.camera_zoom

        if Keyboard.get_pressed(pg.K_a):
            self.camera_position.x -= velocity
        if Keyboard.get_pressed(pg.K_d):
            self.camera_position.x += velocity
        if Keyboard.get_pressed(pg.K_w):
            self.camera_position.y -= velocity
        if Keyboard.get_pressed(pg.K_s):
            self.camera_position.y += velocity
        
        if Keyboard.get_pressed(pg.K_MINUS):
            self.camera_zoom *= 0.98
        if Keyboard.get_pressed(pg.K_EQUALS):
            self.camera_zoom *= 1.02

        self.camera_zoom = clamp(self.camera_zoom, 0.25, 256)

        for i, player in enumerate(self.players):
            # if i > 0:
            #     break
            
            player.update()

    def draw(self) -> None:
        for player in self.players:
            player.draw(self.screen, self.camera_zoom, self.camera_position)

        set_caption(f"{self.clock.get_fps():.2f} fps")

        super().draw()
