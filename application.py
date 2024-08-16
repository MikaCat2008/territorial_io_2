import time
from random import randint
from typing import Optional

import numpy as np
import pygame as pg
from pygame.math import Vector2
from pygame.display import set_mode, set_caption

pg.init()
pg.font.init()

from kit.game import Game
from kit.math import clip, vector2tuple
from kit.pools import PoolManager
from kit.input import Mouse, Keyboard
from kit.graphics import Camera, random_color

from kit.territorial import World, Player


def init_points(x: int, y: int) -> np.matrix:
    return np.array([ (x - 1, y), (x, y - 1), (x, y), (x, y + 1), (x + 1, y) ])


class Application(Game):
    camera: Camera

    world: World
    manager: PoolManager

    selected_id: Optional[int]

    def __init__(self) -> None:
        super().__init__()

        self.screen = set_mode((1500, 750))
        self.camera = Camera(self.screen, 0.7, Vector2(1000, 500))

        self.manager = PoolManager()
        self.manager.start()
        self.world = World(2000, 1000, {}, self.manager)

        for i in range(100):
            self.world.add_player(
                Player(i, random_color(50, 205), self.world, self.manager)
            ).load_territory(init_points(randint(0, 1999), randint(0, 999)))

        self.selected_id = None
        
    def update(self) -> None:
        super().update()

        velocity = 10 / self.camera.zoom

        if Keyboard.get_pressed(pg.K_a):
            self.camera.position.x -= velocity
        if Keyboard.get_pressed(pg.K_d):
            self.camera.position.x += velocity
        if Keyboard.get_pressed(pg.K_w):
            self.camera.position.y -= velocity
        if Keyboard.get_pressed(pg.K_s):
            self.camera.position.y += velocity

        if Mouse.get_clicked(0):
            mouse_pos = self.camera.get_mouse_pos()

            point = vector2tuple(mouse_pos)
            territory_id = self.world.get_point(point)

            if self.selected_id is None:
                if territory_id != 0:
                    self.selected_id = territory_id
            else:
                if territory_id == self.selected_id:
                    self.selected_id = None
                else:
                    player_a = self.world.players.get(self.selected_id)

                    if player_a is None:
                        self.selected_id = None
                    else:
                        if territory_id == 0 or territory_id is None:
                            player_b = None
                        else:
                            player_b = self.world.players.get(territory_id)

                        if player_a.territory.is_alive(_async=False):
                            player_a.expanse(player_b)
                        else:
                            self.selected_id = territory_id

        wheel = Mouse.get_wheel()

        if wheel > 0:
            self.camera.zoom_in()
        if wheel < 0:
            self.camera.zoom_out()

        self.manager.update_futures()

        for player in self.world.players.values():
            player.update()
        
        self.manager.send_input()

    def draw(self) -> None:
        self.world.draw(self.camera, self.selected_id)

        set_caption(f"{self.clock.get_fps():.2f} fps")

        super().draw()
