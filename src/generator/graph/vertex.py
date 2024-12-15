class Vertex:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited = False

    @property
    def x(self) -> int:
        return self.x

    @x.setter
    def x(self, value: int) -> None:
        self.x = value

    @x.deleter
    def x(self) -> None:
        del self.x

    @property
    def y(self) -> int:
        return self.y

    @y.setter
    def y(self, value: int) -> None:
        self.y = value

    @y.deleter
    def y(self) -> None:
        del self.y

    @property
    def visited(self) -> bool:
        return self.visited

    @visited.setter
    def visited(self, value: bool) -> None:
        self.visited = value

    @visited.deleter
    def visited(self) -> None:
        del self.visited
