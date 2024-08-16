from typing import Optional

import pygame as pg
from pygame.time import Clock
from pygame.event import get as get_events
from pygame.display import flip
from pygame.surface import Surface

from kit.input import Mouse, Keyboard


class Game:
    ticks: int
    clock: Clock
    screen: Optional[Surface]
    max_fps: int

    def __init__(self) -> None:
        self.ticks = 0
        self.clock = Clock()
        self.screen = None
        self.max_fps = 60
        
        Mouse()
        Keyboard()

    def initilize(self) -> None:
        Keyboard()

    def update(self) -> None:
        self.ticks += 1
        
        Mouse.update()
        Keyboard.update()

    def draw(self) -> None:
        flip()
        self.screen.fill((0, 0, 0))

    def run(self) -> None:
        self.initilize()

        while 1:
            for event in get_events():
                if event.type == pg.QUIT:
                    exit()

                if event.type == pg.MOUSEWHEEL:
                    Mouse.set_wheel(event.y)

            self.update()
            self.draw()

            self.clock.tick(self.max_fps)
