from pygame.math import Vector2


def tuple2vector(data: tuple[float, float]) -> Vector2:
    return Vector2(data)


def vector2tuple(data: Vector2) -> tuple[float, float]:
    return int(data.x), int(data.y)
