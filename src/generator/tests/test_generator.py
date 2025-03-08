from unittest import TestCase

from src.generator.generator import Generator
from src.generator.graph.graph import Graph
from src.generator.map.map import Map
from src.generator.util.presets import SimplePreset


class TestGenerator(TestCase):

    def setUp(self):
        self.preset = SimplePreset(
            border_width=5,
            mesh_size=3,
            mesh_spacing=10,
            start=(0, 0),
            finish=(3, 3)
        )
        self.map = Map(self.preset)
        self.gen = Generator(self.map)

    def test_create_vertex_mesh(self):
        self.gen.graph = Graph()
        self.gen.create_vertex_mesh()

        self.assertEqual(len(self.gen.graph.vertices), 9)

        all_positions = [
            self.gen.get_vertex_position(x, y)
            for x in range(self.preset.mesh_size)
            for y in range(self.preset.mesh_size)
        ]

        for x, y in all_positions:
            self.assertIsNotNone(self.gen.graph.vertex_at(x, y))

    def test_get_unvisited_neighbours(self):
        self.gen.graph = Graph()
        self.gen.create_vertex_mesh()
        self.gen.graph.set_all_visited(False)

        vertex = self.gen.get_vertex_at(1, 1)

        res = self.gen.get_unvisited_neighbours(vertex)

        self.assertEqual(len(res), 4)
        for v in res:
            self.assertIn(v, self.gen.graph._vertices)


