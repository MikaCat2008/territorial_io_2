from typing import ClassVar, Optional

from pygame import mouse


class MouseState:
    wheel: int
    pressed: tuple[int, int, int]
    
    def __init__(self, wheel: int, pressed: tuple[int, int, int]) -> None:
        self.wheel = wheel
        self.pressed = pressed


class Mouse:
    current_state: Optional[MouseState]
    previous_state: Optional[MouseState]

    _wheel: int

    instance: ClassVar["Mouse"] = None

    def __init__(self) -> None:        
        self.current_state = None
        self.previous_state = None
        
        self._wheel = 0

        Mouse.instance = self

    @classmethod
    def update(cls) -> None:
        self = cls.instance

        previous_state = self.current_state
        self.current_state = MouseState(
            self._wheel, mouse.get_pressed()
        )
        self._wheel = 0

        if previous_state is None:
            self.previous_state = self.current_state
        else:
            self.previous_state = previous_state        

    @classmethod
    def get_pressed(cls, key: int) -> Optional[bool]:
        self = cls.instance
        
        return self.current_state.pressed[key]

    @classmethod
    def get_clicked(cls, key: int) -> Optional[bool]:
        self = cls.instance
        
        return self.current_state.pressed[key] and not self.previous_state.pressed[key]

    @classmethod
    def get_wheel(cls) -> int:
        self = cls.instance
        
        return self.current_state.wheel

    @classmethod
    def set_wheel(cls, value: int) -> None:
        self = cls.instance

        self._wheel = value

    @classmethod
    def get_pos(cls) -> tuple[int, int]:
        return mouse.get_pos()
