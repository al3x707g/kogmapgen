from dataclasses import dataclass

from src.generator.graph.vertex import Vertex


@dataclass(frozen=True)
class Edge:
    v_from: Vertex
    v_to: Vertex

    def has_vertex(self, vertex: Vertex) -> bool:
        return any(
            v is vertex or (v.x == vertex.x and v.y == vertex.y)
            for v in (self.v_to, self.v_from)
        )
