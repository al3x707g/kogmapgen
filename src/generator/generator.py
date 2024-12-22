from src.generator.util.blocks import BlockType
from src.generator.util.types import GRID


class Generator:
    grid: GRID

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.fill_grid(BlockType.HOOKABLE)

    def fill_grid(self, block_type: BlockType) -> GRID:
        grid: GRID = [
            [block_type for _ in range(self.width)]
            for _ in range(self.height)
        ]

        self.grid = grid
