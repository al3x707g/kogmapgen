from unittest import TestCase

from src.generator.graph.edge import Edge
from src.generator.graph.vertex import Vertex


class TestEdge(TestCase):

    def setUp(self):
        self.vertex_from = Vertex(5, 1)
        self.vertex_to = Vertex(3, 7)
        self.edge = Edge(self.vertex_from, self.vertex_to)

    def test_has_vertex(self):
        self.assertTrue(self.edge.has_vertex(self.vertex_from))
        self.assertTrue(self.edge.has_vertex(self.vertex_to))

        # a vertex should be recognisable by the coordinates, too, rather than the vertex object specifically
        self.assertTrue(self.edge.has_vertex(Vertex(5, 1)))
        self.assertTrue(self.edge.has_vertex(Vertex(3, 7)))

        # twisted coordinates can not represent the same vertex
        self.assertFalse(self.edge.has_vertex(Vertex(1, 5)))
        self.assertFalse(self.edge.has_vertex(Vertex(7, 3)))
