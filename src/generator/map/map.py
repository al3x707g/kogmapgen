import numpy as np

from PIL import ImageColor, Image
from src.generator.util.blocks import BlockType, BlockColor
from src.generator.util.presets import SimplePreset
from src.generator.util.types import GRID


class Map:
    grid: GRID

    def __init__(self, preset: SimplePreset) -> None:
        self.preset = preset
        self.grid_size = preset.mesh_spacing * (preset.mesh_size + 1)
        self.create_empty_grid(BlockType.HOOKABLE)

    def create_empty_grid(self, block_type: BlockType) -> GRID:
        grid: GRID = [
            [block_type for _ in range(self.grid_size)]
            for _ in range(self.grid_size)
        ]

        self.grid = grid

    def get_padded_np_array(self):
        border_width = self.preset.border_width

        np_arr = np.array(self.grid)
        colored_arr = np.array(
            [
                [ImageColor.getcolor(BlockColor.get(block), "RGB") for block in row]
                for row in np_arr
            ],
            dtype=np.uint8
        )

        rows, cols, _ = colored_arr.shape
        new_shape = (rows + 2 * border_width, cols + 2 * border_width, 3)

        padded_array = np.full(
            new_shape,
            ImageColor.getcolor(BlockColor.get(BlockType.FLOOD), "RGB"),
            dtype=np.uint8
        )

        padded_array[border_width:-border_width, border_width:-border_width] = colored_arr

        return padded_array

    def save_image(self) -> None:
        if self.grid:
            arr = self.get_padded_np_array()
            image = Image.fromarray(arr)
            image.save("map.png")
