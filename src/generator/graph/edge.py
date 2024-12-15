from vertex import Vertex


class Edge:

    def __init__(self, v_from: Vertex, v_to: Vertex):
        self.v_from = v_from
        self.v_to = v_to

    def has_vertex(self, vertex: Vertex) -> bool:
        if not vertex:
            return False

        return any(
            v is vertex or (v.x == vertex.x and v.y == vertex.y)
            for v in (self.v_to, self.v_from)
        )

    @property
    def v_from(self) -> Vertex:
        return self.v_from

    @v_from.setter
    def v_from(self, value: Vertex) -> None:
        self.v_from = value

    @v_from.deleter
    def v_from(self) -> None:
        del self.v_from

    @property
    def v_to(self) -> Vertex:
        return self.v_to

    @v_to.setter
    def v_to(self, value: Vertex) -> None:
        self.v_to = value

    @v_to.deleter
    def v_to(self) -> None:
        del self.v_to
