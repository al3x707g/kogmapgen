from src.generator.util.blocks import BlockType
from src.generator.util.types import GRID


class Generator:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid: GRID = self.get_filled_grid(BlockType.HOOKABLE)

    def get_filled_grid(self, block_type: BlockType) -> GRID:
        grid: GRID = [
            [block_type for _ in range(self.width)]
            for _ in range(self.height)
        ]

        return grid
