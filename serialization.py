import json

from pygame.math import Vector2, Vector3

from polygon import Polygon


def create_save(polygons: list[Polygon]) -> None:
    with open("saves/current.save", "w") as f:
        json.dump([
            {
                "color": [
                    int(polygon.color.x), 
                    int(polygon.color.y), 
                    int(polygon.color.z)
                ],
                "vertices": [
                    [
                        int(node.value.x), 
                        int(node.value.y)
                    ]
                    for node in polygon.vertices
                ]
            }
            for polygon in polygons
        ], f)


def open_save() -> list[Polygon]:
    with open("saves/current.save") as f:
        return [
            Polygon(
                color=Vector3(polygon["color"]),
                vertices=[
                    Vector2(vertex)
                    for vertex in polygon["vertices"]
                ]
            )
            for polygon in json.load(f)
        ]
