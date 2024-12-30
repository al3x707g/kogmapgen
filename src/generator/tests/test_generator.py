from unittest import TestCase

from src.generator.generator import Generator
from src.generator.graph.graph import Graph
from src.generator.map.map import Map
from src.generator.util.presets import Preset


class TestGenerator(TestCase):

    def setUp(self):
        self.preset = Preset(
            border_width=10,
            grid_width=200,
            grid_height=400,
            mesh_size=3,
            end_x=0,  # not yet implemented, can be ignored
            end_y=0,  # not yet implemented, can be ignored
            start_x=0,  # not yet implemented, can be ignored
            start_y=0,  # not yet implemented, can be ignored
            min_width=0,  # not yet implemented, can be ignored
            max_play=0,  # not yet implemented, can be ignored
        )
        self.map = Map(self.preset)
        self.gen = Generator(self.map)

    def test_create_vertex_mesh(self):
        self.gen.graph = Graph()
        self.gen.create_vertex_mesh()

        self.assertEqual(len(self.gen.graph.vertices), 9)
