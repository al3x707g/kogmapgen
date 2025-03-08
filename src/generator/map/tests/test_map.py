from unittest import TestCase

from src.generator.map.map import Map
from src.generator.util.blocks import BlockType
from src.generator.util.presets import SimplePreset


class TestMap(TestCase):

    def setUp(self):
        self.preset = SimplePreset(
            border_width=5,
            mesh_size=3,
            mesh_spacing=10,
            start=(0, 0),
            finish=(3, 3)
        )
        self.map = Map(self.preset)

    def test_empty_grid_created(self):
        # constructor calls create_empty_grid, no need to explicitly call it again

        # Check if every block in the grid is of block type hookable
        for row in self.map.grid:
            for block in row:
                self.assertEqual(block, BlockType.HOOKABLE)
