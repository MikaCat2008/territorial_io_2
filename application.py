import pygame as pg
from pygame.display import set_mode, set_caption

pg.init()
pg.font.init()

from kit.game import Game
from kit.utils import PoolObject
from player import Player


class Application(Game):
    def __init__(self) -> None:
        super().__init__()

        PoolObject.create_pool()

        self.screen = set_mode((1200, 600))
        self.players = [ Player() ]
        self.players[0].load_points({
            (24, 25), (25, 24), (25, 25), (25, 26), (26, 25)    
        })

    def update(self) -> None:
        super().update()

        for player in self.players:
            player.update()

    def draw(self) -> None:
        for player in self.players:
            player.draw(self.screen)

        set_caption(f"{self.clock.get_fps():.2f} fps")

        super().draw()
