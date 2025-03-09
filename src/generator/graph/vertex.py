from dataclasses import dataclass


@dataclass
class Vertex:
    x: int
    y: int
    visited: bool = False

    def __eq__(self, other):
        if isinstance(other, Vertex):
            return (self.x, self.y) == (other.x, other.y)
        return False

    def __hash__(self):
        return hash((self.x, self.y))
