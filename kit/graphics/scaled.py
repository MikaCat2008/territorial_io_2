import pygame as pg
from pygame.draw import lines, polygon
from pygame.math import Vector2
from pygame.surface import Surface
from pygame.transform import scale_by

from kit.math import max_vector, get_vertices_bounds

from .color import Color


def get_bounds(
    size: Vector2, 
    offset: Vector2, 
    max_size: Vector2,
    min_vertex: Vector2
) -> tuple[Vector2, Vector2]:
    min_bounds = max_vector(
        Vector2(), -offset - min_vertex
    ) // 1
    max_bounds = max_vector(
        Vector2(), min_vertex + size + offset - max_size
    ) // 1

    return min_bounds, max_bounds


def blit_scaled_in_bounds(
    screen: Surface,
    size: Vector2,
    scale: float,
    offset: Vector2,
    surface: Surface,
    min_vertex: Vector2
) -> None:
    min_bounds, max_bounds = get_bounds(
        size, offset, Vector2(screen.get_size()) // scale, min_vertex
    )

    size -= min_bounds + max_bounds

    if size.x < 0 or size.y < 0:
        return

    new_surface = Surface(size + Vector2(1), pg.SRCALPHA)
    new_surface.blit(surface, -min_bounds)

    screen.blit(
        scale_by(new_surface, scale), 
        offset * scale + min_vertex * scale + min_bounds * scale
    )


def scaled_lines(
    screen: Surface,
    scale: float,
    color: Color,
    offset: Vector2,
    vertices: list[Vector2]
) -> None:
    min_vertex, max_vertex = get_vertices_bounds(vertices)

    if min_vertex is None:
        return

    size = max_vertex - min_vertex + Vector2(1) 
    surface = Surface(size, pg.SRCALPHA)

    lines(surface, color, False, [vertex - min_vertex for vertex in vertices])
    blit_scaled_in_bounds(
        screen, size, scale, offset, surface, min_vertex
    )


def scaled_polygon(
    screen: Surface,
    scale: float,
    color: Color,
    offset: Vector2,
    vertices: list[Vector2]
) -> None:    
    min_vertex, max_vertex = get_vertices_bounds(vertices)

    if min_vertex is None:
        return

    size = max_vertex - min_vertex + Vector2(1) 
    surface = Surface(size, pg.SRCALPHA)

    polygon(surface, color, [vertex - min_vertex for vertex in vertices])
    blit_scaled_in_bounds(
        screen, size, scale, offset, surface, min_vertex
    )
