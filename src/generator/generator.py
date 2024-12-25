import random

from src.generator.graph.edge import Edge
from src.generator.graph.graph import Graph
from src.generator.graph.vertex import Vertex
from src.generator.map.map import Map


class Generator:
    graph: Graph

    def __init__(self, game_map: Map) -> None:
        self.map = game_map
        self.preset = game_map.preset
        self.distance_x, self.distance_y = self.map.get_distances()

    def generate_from_graph(self) -> None:
        self.graph = Graph()

        self.create_vertex_mesh()

    def create_vertex_mesh(self) -> None:
        if not self.graph:
            return

        border = self.preset.border_width
        mesh_size = self.preset.mesh_size

        [self.graph.add_vertex(
            Vertex(
                border + self.distance_x * x,
                border + self.distance_y * y
            )
        ) for x in range(mesh_size) for y in range(mesh_size)]

    def connect_graph_random(self) -> None:
        self.graph.set_all_visited(False)

        start_x = self.preset.border_width + self.preset.start_x + self.distance_x
        start_y = self.preset.border_width + self.preset.start_y + self.distance_y

        v_start = self.graph.vertex_at(start_x, start_y)

        stack = []
        current = v_start

        stack.append(current)

        while stack:
            if current is None:
                return

            current.visited = True

            neighbours = self.get_unvisited_neighbours(current)
            if neighbours:
                next_vertex = random.choice(neighbours)

                edge = Edge(current, next_vertex)
                self.graph.add_edge(edge)

                current = next_vertex
                stack.append(current)
            else:
                stack.pop()
                if stack:
                    current = stack[-1]

    def get_unvisited_neighbours(self, vertex: Vertex) -> list[Vertex]:
        potential_neighbours = [
            self.get_vertex_by_offset(vertex, -1, 0),
            self.get_vertex_by_offset(vertex, 1, 0),

            self.get_vertex_by_offset(vertex, 0, -1),
            self.get_vertex_by_offset(vertex, 0, 1)
        ]

        filtered_neighbours = list(
            filter(
                lambda v: v is not None and not v.visited,
                potential_neighbours
            )
        )

        return filtered_neighbours

    def get_vertex_by_offset(self, vertex: Vertex, offset_x: int, offset_y: int) -> Vertex | None:
        border_width = self.preset.border_width

        # Calculate the target vertex coordinates
        target_x = border_width + vertex.x + self.distance_x * offset_x
        target_y = border_width + vertex.y + self.distance_y * offset_y

        # Check if the vertex is within the border of the grid
        if not border_width < target_x < self.preset.grid_width - border_width:
            return None

        if not border_width < target_y < self.preset.grid_height - border_width:
            return None

        return Vertex(target_x, target_y)
