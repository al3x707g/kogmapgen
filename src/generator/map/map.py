from src.generator.util.blocks import BlockType
from src.generator.util.presets import Preset
from src.generator.util.types import GRID


class Map:
    grid: GRID

    def __init__(self, preset: Preset) -> None:
        self.preset = preset
        self.fill_grid(BlockType.HOOKABLE)

    def fill_grid(self, block_type: BlockType) -> GRID:
        grid: GRID = [
            [block_type for _ in range(self.preset.grid_width)]
            for _ in range(self.preset.grid_height)
        ]

        self.grid = grid

    def get_distances(self) -> tuple[int, int]:
        calc_distance = lambda val: int((val - 2 * self.preset.border_width) / (self.preset.mesh_size - 1))

        distance_x = calc_distance(self.preset.grid_width)
        distance_y = calc_distance(self.preset.grid_height)

        return distance_x, distance_y
