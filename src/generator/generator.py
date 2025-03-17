import random

import numpy as np

from noise import pnoise1
from scipy.interpolate import interp1d
from src.generator.graph.edge import Edge
from src.generator.graph.graph import Graph
from src.generator.graph.vertex import Vertex
from src.generator.map.map import Map
from src.generator.util.blocks import BlockType
from src.generator.util.utilities import bresenham_line
from src.generator.util.utilities import generate_widths
from typing import Literal


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
        self.paint_smooth_path()

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

        unreferenced_edges = [edge for edge in self.graph.edges.values() if edge not in path]

        for edge in unreferenced_edges:
            if self.graph.has_edge(edge):
                self.graph.delete_edge(edge)

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

    def paint_grouped_edges(self, method: str = None | Literal["perlin"]):
        for edge in self.group_edges():
            match method:
                case "perlin":
                    self.paint_edge_perlin(edge)
                case _:
                    self.paint_edge(edge)

    def paint_edge_perlin(self, edge: Edge, scale=0.07, amplitude=4) -> None:
        vertical = edge.is_vertical()

        # get start and end vertex position
        start, end = sorted([edge.v_from.y, edge.v_to.y] if vertical else [edge.v_from.x, edge.v_to.x])

        # base is base coordinate the offset is applied to
        base = edge.v_to.x if vertical else edge.v_to.y

        for i, c in enumerate(range(start, end)):
            # get offset using perlin noise
            noise = pnoise1(i * scale)
            offset = int(noise * amplitude)

            # calculate new position by applying the offset to the base position
            pos = base + offset

            if vertical:
                self.map.grid[c][pos - 2] = BlockType.EMPTY
                self.map.grid[c][pos - 1] = BlockType.EMPTY
                self.map.grid[c][pos] = BlockType.EMPTY
            else:
                self.map.grid[pos - 2][c] = BlockType.EMPTY
                self.map.grid[pos - 1][c] = BlockType.EMPTY
                self.map.grid[pos][c] = BlockType.EMPTY

    def paint_edge(self, edge: Edge) -> None:
        vertical = edge.is_vertical()

        start, end = sorted([edge.v_from.y, edge.v_to.y] if vertical else [edge.v_from.x, edge.v_to.x])

        for c in range(start, end):
            if vertical:
                self.map.grid[c][edge.v_to.x - 2] = BlockType.FLOOD
                self.map.grid[c][edge.v_to.x - 1] = BlockType.FLOOD
                self.map.grid[c][edge.v_to.x] = BlockType.FLOOD
            else:
                self.map.grid[edge.v_to.y - 2][c] = BlockType.FLOOD
                self.map.grid[edge.v_to.y - 1][c] = BlockType.FLOOD
                self.map.grid[edge.v_to.y][c] = BlockType.FLOOD

    def group_edges(self):
        edge_groups = self.get_continuous_edge_groups()

        result = []

        for group in edge_groups:
            is_vertical = group[0].is_vertical()

            if is_vertical:
                lowest_vertex = min((v for edge in group for v in (edge.v_to, edge.v_from)), key=lambda v: v.y)
                highest_vertex = max((v for edge in group for v in (edge.v_to, edge.v_from)), key=lambda v: v.y)
            else:
                lowest_vertex = min((v for edge in group for v in (edge.v_to, edge.v_from)), key=lambda v: v.x)
                highest_vertex = max((v for edge in group for v in (edge.v_to, edge.v_from)), key=lambda v: v.x)

            result.append(Edge(lowest_vertex, highest_vertex))

        return result

    def get_continuous_edge_groups(self):
        result = []
        visited_edges = set()

        for edge in self.graph.edges.values():
            if edge in visited_edges:
                continue

            stack, group = [edge.v_from], []
            is_vertical = None

            while stack:
                vertex = stack.pop()

                for neighbor in self.graph.adjacency[vertex]:
                    edge = self.graph.find_edge(vertex, neighbor)
                    if edge and edge not in visited_edges:
                        if is_vertical is None:
                            is_vertical = edge.is_vertical()

                        if edge.is_vertical() == is_vertical:
                            group.append(edge)
                            visited_edges.add(edge)
                            stack.append(neighbor)

            if group:
                result.append(group)

        return result

    def calculate_catmull_rom_splines(self) -> list[Vertex]:
        vertices = [v for v in self.graph.adjacency.keys()]

        if len(vertices) < 4:
            return vertices  # Not enough points for interpolation

        x_vals, y_vals = zip(*[(v.x, v.y) for v in vertices])

        t = np.linspace(0, 1, len(vertices))
        interp_x = interp1d(t, x_vals, kind="cubic")
        interp_y = interp1d(t, y_vals, kind="cubic")

        smooth_t = np.linspace(0, 1, len(vertices) * 5)
        smooth_x = interp_x(smooth_t)
        smooth_y = interp_y(smooth_t)

        return [Vertex(int(x), int(y)) for x, y in zip(smooth_x, smooth_y)]

    def paint_connected_vertices(self, vertices: list[Vertex]) -> None:
        # generate different widths for every vertex
        widths = generate_widths(len(vertices))

        for i in range(len(vertices) - 1):
            line_points = bresenham_line(vertices[i], vertices[i + 1])

            width = widths[i]

            for x, y in line_points:
                for dx in range(-width, width + 1):
                    for dy in range(-width, width + 1):
                        self.map.grid[y + dy][x + dx] = BlockType.EMPTY

    def paint_smooth_path(self):
        vertices = self.calculate_catmull_rom_splines()
        self.paint_connected_vertices(vertices)

    @staticmethod
    def get_vertex_coordinates(vertex: Vertex) -> tuple[int, int]:
        return vertex.x - 1 if vertex.x > 0 else 0, vertex.y - 1 if vertex.y > 0 else 0
