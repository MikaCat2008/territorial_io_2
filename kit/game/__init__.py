from typing import Optional

import pygame as pg
from pygame.time import Clock
from pygame.event import get as get_events
from pygame.display import flip
from pygame.surface import Surface

from kit.input import Keyboard


class Game:
    clock: Clock
    max_fps: int

    screen: Optional[Surface]

    def __init__(self) -> None:
        self.clock = Clock()
        self.ticks = 0
        self.max_fps = 60

        self.screen = None

    def initilize(self) -> None:
        Keyboard()

    def update(self) -> None:
        Keyboard.update()
        self.ticks += 1

    def draw(self) -> None:
        flip()
        self.screen.fill((0, 0, 0))

    def run(self) -> None:
        self.initilize()

        while 1:
            for event in get_events():
                if event.type == pg.QUIT:
                    exit()

            self.update()
            self.draw()

            self.clock.tick(self.max_fps)
