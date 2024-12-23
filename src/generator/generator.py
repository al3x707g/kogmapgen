from src.generator.graph.graph import Graph
from src.generator.graph.vertex import Vertex
from src.generator.map.presets import Preset
from src.generator.util.blocks import BlockType
from src.generator.util.types import GRID


class Generator:
    grid: GRID
    graph: Graph

    def __init__(self, preset: Preset) -> None:
        self.preset = preset

        self.fill_grid(BlockType.HOOKABLE)

    def fill_grid(self, block_type: BlockType) -> GRID:
        grid: GRID = [
            [block_type for _ in range(self.preset.grid_width)]
            for _ in range(self.preset.grid_height)
        ]

        self.grid = grid

    def generate_from_graph(self) -> None:
        self.graph = Graph()

        self.create_vertex_mesh()
        # TBD

    def create_vertex_mesh(self) -> None:
        if not self.graph:
            return

        border = self.preset.border_width
        mesh_size = self.preset.mesh_size

        distance_x, distance_y = self.get_distances()

        [self.graph.add_vertex(
            Vertex(
                border + distance_x * x,
                border + distance_y * y
            )
        ) for x in range(mesh_size) for y in range(mesh_size)]

    def get_distances(self) -> tuple[int, int]:
        calc_distance = lambda val: int((val - 2 * self.preset.border_width) / (self.preset.mesh_size - 1))

        distance_x = calc_distance(self.preset.grid_width)
        distance_y = calc_distance(self.preset.grid_height)

        return distance_x, distance_y
