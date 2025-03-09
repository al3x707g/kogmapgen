import random

from src.generator.graph.edge import Edge
from src.generator.graph.graph import Graph
from src.generator.graph.vertex import Vertex
from src.generator.map.map import Map
from src.generator.util.blocks import BlockType


class Generator:
    graph: Graph

    def __init__(self, game_map: Map) -> None:
        self.map = game_map
        self.preset = game_map.preset
        self.spacing = game_map.preset.mesh_spacing

    def generate_from_graph(self) -> None:
        self.graph = Graph()

        self.create_vertex_mesh()
        self.connect_graph_random()
        self.find_path()

    def create_vertex_mesh(self) -> None:
        if not self.graph:
            return

        mesh_size = self.preset.mesh_size + 1

        [self.graph.add_vertex(self.spacing * x, self.spacing * y)
         for x in range(1, mesh_size) for y in range(1, mesh_size)]

    def connect_graph_random(self) -> None:
        self.graph.set_all_visited(False)

        v_start = self.get_vertex_at(self.preset.start[0], self.preset.start[1])

        history = [v_start]
        current = history[0]

        while history:
            if current is None:
                break

            current.visited = True

            neighbours = self.get_unvisited_neighbours(current)
            if neighbours:
                next_vertex = random.choice(neighbours)

                edge = Edge(current, next_vertex)
                self.graph.add_edge(edge)

                current = next_vertex
                history.append(current)
            else:
                history.pop()
                if history:
                    current = history[-1]

    def find_path(self):
        v_start = self.get_vertex_at(*self.preset.start)
        v_finish = self.get_vertex_at(*self.preset.finish)

        path = self.graph.dfs(v_start, v_finish)

        self.graph.edges = {
            key: edge for key, edge in self.graph.edges.items() if edge in path
        }

    def get_unvisited_neighbours(self, vertex: Vertex) -> list[Vertex]:
        neighbour_positions = [
            (-1, 0), (1, 0),  # left and right
            (0, -1), (0, 1)  # up and down
        ]

        potential_neighbours = [
            self.get_vertex_by_offset(vertex, x, y)
            for x, y in neighbour_positions
        ]

        filtered_neighbours = list(
            filter(
                lambda v: v is not None and not v.visited,
                potential_neighbours
            )
        )

        return filtered_neighbours

    def get_vertex_by_offset(self, vertex: Vertex, offset_x: int, offset_y: int) -> Vertex | None:
        # Calculate the target vertex coordinates
        target_x = vertex.x + self.spacing * offset_x
        target_y = vertex.y + self.spacing * offset_y

        res = self.graph.vertex_at(target_x, target_y)

        return res

    def get_vertex_at(self, mesh_x: int, mesh_y: int) -> Vertex | None:
        # Calculate the target vertex coordinates
        target_x = self.spacing * (mesh_x + 1)
        target_y = self.spacing * (mesh_y + 1)

        res = self.graph.vertex_at(target_x, target_y)

        return res

    def get_vertex_position(self, mesh_x: int, mesh_y: int) -> tuple[int, int] | None:
        # Calculate the target vertex coordinates
        target_x = self.spacing * (mesh_x + 1)
        target_y = self.spacing * (mesh_y + 1)

        return target_x, target_y

    def paint_all_vertices(self):
        for vertex in self.graph.vertices.values():
            x, y = self.get_vertex_coordinates(vertex)
            self.map.grid[x][y] = BlockType.FLOOD

    def paint_all_edges(self):
        for edge in self.graph.edges.values():
            self.paint_edge(edge)

    def paint_edge(self, edge: Edge) -> None:
        if edge.v_from.x == edge.v_to.x:  # Vertical edge
            y_start, y_end = sorted([edge.v_from.y, edge.v_to.y])
            for y in range(y_start, y_end):
                self.map.grid[y][edge.v_to.x - 2] = BlockType.FLOOD
                self.map.grid[y][edge.v_to.x - 1] = BlockType.FLOOD
                self.map.grid[y][edge.v_to.x] = BlockType.FLOOD

        elif edge.v_from.y == edge.v_to.y:  # Horizontal edge
            x_start, x_end = sorted([edge.v_from.x, edge.v_to.x])
            for x in range(x_start, x_end):
                self.map.grid[edge.v_to.y - 2][x] = BlockType.FLOOD
                self.map.grid[edge.v_to.y - 1][x] = BlockType.FLOOD
                self.map.grid[edge.v_to.y][x] = BlockType.FLOOD

    @staticmethod
    def get_vertex_coordinates(vertex: Vertex) -> tuple[int, int]:
        return vertex.x - 1 if vertex.x > 0 else 0, vertex.y - 1 if vertex.y > 0 else 0
