from collections import defaultdict

from src.generator.graph.edge import Edge
from src.generator.graph.vertex import Vertex


class Graph:

    def __init__(self):
        """
        Creates an empty graph.
        """
        self.vertices: dict[tuple[int, int], Vertex] = {}
        self.edges: dict[tuple[Vertex, Vertex], Edge] = {}
        self.adjacency: dict[Vertex, list[Vertex]] = defaultdict(list)

    def vertex_at(self, x: int, y: int) -> Vertex | None:
        """
        Checks whether a vertex exists at the given coordinates.
        :param x: The x coordinate of the vertex.
        :param y: The y coordinate of the vertex.
        :return: The vertex from the graph if found, otherwise None.
        """
        return self.vertices.get((x, y), None)

    def has_vertex(self, vertex: Vertex) -> bool:
        """
        Checks whether the graph contains a vertex.
        :param vertex: The vertex to be checked for.
        :return: True if the vertex is found in the graph, otherwise False.
        """
        return vertex in self.vertices.values()

    def add_vertex(self, x: int, y: int) -> None:
        """
        Adds a vertex to the graph.
        :param x: The x coordinate of the vertex.
        :param y: The y coordinate of the vertex.
        """
        if not self.vertex_at(x, y):
            self.vertices[(x, y)] = Vertex(x, y)

    def delete_vertex(self, vertex: Vertex) -> None:
        """
        Deletes a vertex from the graph and removes any edge associated with this vertex.
        :param vertex: The vertex to be deleted.
        """
        vertex_key = (vertex.x, vertex.y)

        if vertex_key in self.vertices:
            del self.vertices[vertex_key]

            if vertex in self.adjacency:
                for neighbor in list(self.adjacency[vertex]):
                    edge_key = (vertex, neighbor) if (vertex, neighbor) in self.edges else (neighbor, vertex)
                    if edge_key in self.edges:
                        del self.edges[edge_key]
                    self.adjacency[neighbor].remove(vertex)

                del self.adjacency[vertex]

    def has_edge(self, edge: Edge) -> bool:
        """
        Checks whether the graph contains an edge.
        :param edge: The edge to be checked for.
        :return: True if the edge is found in the graph, otherwise False.
        """
        return (edge.v_from, edge.v_to) in self.edges or (edge.v_to, edge.v_from) in self.edges

    def find_edge(self, v_from: Vertex, v_to: Vertex) -> Edge | None:
        """
        Finds an edge connecting two vertices in the graph.
        :param v_from: The starting vertex of the edge.
        :param v_to: The ending vertex of the edge.
        :return: The edge connecting the two vertices, or None if no such edge exists.
        """
        if v_to in self.adjacency.get(v_from, []):
            return self.edges.get((v_from, v_to)) or self.edges.get((v_to, v_from))
        return None

    def add_edge(self, edge: Edge) -> None:
        """
        Adds an edge to the graph. If the edge's vertices are not yet part of the graph, they are added too.
        :param edge: The edge to be added.
        """
        if edge.v_to == edge.v_from or (edge.v_from, edge.v_to) in self.edges:
            return

        self.edges[(edge.v_from, edge.v_to)] = edge
        self._add_missing_vertices(edge)

        self.adjacency[edge.v_from].append(edge.v_to)
        self.adjacency[edge.v_to].append(edge.v_from)

    def delete_edge(self, edge: Edge) -> None:
        """
        Deletes an edge from the graph and removes the edge's vertices, that are not referenced by any other edge.
        :param edge: The edge to be removed.
        """
        edge_key = (edge.v_from, edge.v_to)

        if edge_key not in self.edges:
            return

        del self.edges[edge_key]

        self.adjacency[edge.v_from].remove(edge.v_to)
        self.adjacency[edge.v_to].remove(edge.v_from)

        for vertex in (edge.v_from, edge.v_to):
            if not self.is_vertex_referenced(vertex):
                self.delete_vertex(vertex)

    def find_neighbours(self, vertex: Vertex) -> list[Vertex]:
        """
        Finds all vertices connected to the vertex with an edge.
        :param vertex: The vertex to be checked with.
        :return: A list of neighbours, or an empty list if there are none.
        """
        return self.adjacency.get(vertex, [])

    def has_neighbours(self, vertex: Vertex) -> bool:
        """
        Checks whether the given vertex has any edges connecting it to other vertices.
        :param vertex: The vertex to be checked.
        :return: True if the vertex has any neighbours, otherwise False.
        """
        return vertex in self.adjacency and bool(self.adjacency[vertex])

    def has_unvisited_neighbours(self, vertex: Vertex) -> bool:
        """
        Checks whether the given vertex has any edges connecting it to other unvisited vertices.
        :param vertex: The vertex to be checked.
        :return: True if the vertex has any unvisited neighbours, otherwise False.
        """
        neighbours = self.find_neighbours(vertex)

        for neighbour in neighbours:
            if not neighbour.visited:
                return True

        return False

    def is_vertex_referenced(self, vertex: Vertex) -> bool:
        """
        Checks whether the given vertex is referenced by any edge in the graph.
        :param vertex: The vertex to check for.
        :return: True if the vertex is part of at least one edge, otherwise False.
        """
        return bool(self.adjacency.get(vertex, None))

    def set_all_visited(self, visited: bool) -> None:
        """
        Changes the `visited` value for every vertex in the graph.
        :param visited: The value to change the `visited` value to.
        """
        for vertex in self.vertices.values():
            vertex.visited = visited

    def all_visited(self, visited: bool) -> bool:
        """
        Checks if all vertices in the graph are visited.
        :param visited: Can be True to check if all vertices are visited, or False to check if none are visited.
        :return: True if all vertices' visited state match the `visited` parameter, otherwise False.
        """
        for vertex in self.vertices.values():
            if vertex.visited is not visited:
                return False

        return True

    def dfs(self, from_vertex: Vertex, to_vertex: Vertex) -> list[Edge] | None:
        """Perform a depth-first search from `from_vertex` to `to_vertex` and return the path as a list of edges."""
        if not from_vertex or not to_vertex:
            return None

        self.set_all_visited(False)

        result = []
        stack = [from_vertex]
        from_vertex.visited = True

        current = from_vertex
        next_vertex = None

        while current != to_vertex and stack:
            current.visited = True
            if self.has_unvisited_neighbours(current):
                neighbours = self.find_neighbours(current)

                for neighbour in neighbours:
                    if not neighbour.visited:
                        next_vertex = neighbour
                        break

                stack.append(next_vertex)
                current = next_vertex
            else:
                stack.pop()
                if stack:
                    current = stack[-1]

        while stack:
            edge_from = stack.pop()
            edge_to = stack[-1] if stack else None

            if edge_to:
                result.append(self.find_edge(edge_from, edge_to))

        return result

    def _add_missing_vertices(self, edge: Edge) -> None:
        for vertex in (edge.v_from, edge.v_to):
            if (vertex.x, vertex.y) not in self.vertices:
                self.vertices[(vertex.x, vertex.y)] = vertex
