from unittest import TestCase

from src.generator.map.map import Map
from src.generator.util.blocks import BlockType
from src.generator.util.presets import Preset


class TestMap(TestCase):

    def setUp(self):
        self.preset = Preset(
            border_width=10,
            grid_width=200,
            grid_height=400,
            mesh_size=12,
            end_x=0,  # not yet implemented, can be ignored
            end_y=0,  # not yet implemented, can be ignored
            start_x=0,  # not yet implemented, can be ignored
            start_y=0,  # not yet implemented, can be ignored
            min_width=0,  # not yet implemented, can be ignored
            max_play=0,  # not yet implemented, can be ignored
        )
        self.map = Map(self.preset)

    def test_fill_grid(self):
        # constructor calls fill_grid, no need to explicitly call it again

        # Check if every block in the grid is of block type hookable
        for i in range(self.preset.grid_width):
            for j in range(self.preset.grid_height):
                self.assertEqual(self.map.grid[j][i], BlockType.HOOKABLE)

    def test_get_distances(self):
        distance_x, distance_y = self.map.get_distances()

        self.assertEqual(distance_x, 13)
        self.assertEqual(distance_y, 29)
