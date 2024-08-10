from kit.utils import in_pool, PoolObject


class Territory(PoolObject):
    points: set[tuple[int, int]]

    def __init__(self, id: int) -> None:
        super().__init__(id)

        self.points = set()

    @in_pool
    def expanse(self) -> set[tuple[int, int]]:
        self.points.add(self.id)

        return self.points


if __name__ == "__main__":
    PoolObject.create_pool()

    t1 = Territory.link()
    t2 = Territory.link()

    print(t1.expanse())
    print(t2.expanse())
