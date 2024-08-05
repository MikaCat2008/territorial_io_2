from typing import ClassVar, Optional

from pygame import key


class Keyboard:
    current_state: key.ScancodeWrapper
    previous_state: key.ScancodeWrapper

    instance: ClassVar["Keyboard"] = None

    def __init__(self) -> None:
        self.current_state = key.get_pressed()
        self.previous_state = self.current_state
        
        Keyboard.instance = self

    @classmethod
    def update(cls) -> None:
        self = cls.instance

        self.previous_state = self.current_state
        self.current_state = key.get_pressed()

    @classmethod
    def get_pressed(cls, key: int) -> Optional[bool]:
        self = cls.instance
        
        return self.current_state[key]

    @classmethod
    def get_clicked(cls, key: int) -> Optional[bool]:
        self = cls.instance
        
        return self.current_state[key] and not self.previous_state[key]
