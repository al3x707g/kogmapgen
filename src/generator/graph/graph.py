from vertex import Vertex
from edge import Edge


class Graph:

    def __init__(self):
        """
        Creates an empty graph.
        """
        self._vertices = []
        self._edges = []

    @property
    def vertices(self) -> list[Vertex]:
        return self._vertices[:]

    @property
    def edges(self) -> list[Edge]:
        return self._edges[:]

    def vertex_at(self, x: int, y: int) -> Vertex | None:
        """
        Checks whether a vertex exists at the given coordinates.
        :param x: The x coordinate of the vertex.
        :param y: The y coordinate of the vertex.
        :return: The vertex from the graph if found, otherwise None.
        """
        for vertex in self.vertices:
            if vertex.x == x and vertex.y == y:
                return vertex

        return None

    def find_vertex(self, vertex: Vertex) -> Vertex | None:
        """
        Checks for an existing vertex in the graph and returns the vertex object if found.
        :param vertex: The vertex to be checked for.
        :return: The vertex from the existing graph if found, otherwise None.
        """
        vertex_obj = self.vertex_at(vertex.x, vertex.y) if vertex not in self.vertices else vertex

        if vertex_obj:
            return vertex_obj

    def has_vertex(self, vertex: Vertex) -> bool:
        """
        Checks whether the graph contains a vertex.
        :param vertex: The vertex to be checked for.
        :return: True if the vertex is found in the graph, otherwise False.
        """
        return vertex in self.vertices or self.find_vertex(vertex) is not None

    def add_vertex(self, vertex: Vertex) -> None:
        """
        Adds a vertex to the graph.
        :param vertex: The vertex to be added.
        """
        if not self.has_vertex(vertex):
            self._vertices.append(vertex)

    def delete_vertex(self, vertex: Vertex) -> None:
        """
        Deletes a vertex from the graph and removes any edge associated with this vertex.
        :param vertex: The vertex to be deleted.
        """
        if not self.has_vertex(vertex):
            return

        try:
            if vertex in self.vertices:
                self._vertices.remove(vertex)
            else:
                self._vertices.remove(self.vertex_at(vertex.x, vertex.y))

            for edge in self._edges:
                if vertex in (edge.v_from, edge.v_to):
                    self.delete_edge(edge)
        except ValueError:
            print("An unexpected error has occurred trying to remove a vertex.")

    def find_edge(self, edge: Edge) -> Edge | None:
        """
        Checks for an existing edge in the graph and returns the edge object if found.
        :param edge: The edge to be checked for.
        :return: The edge from the existing graph if found, otherwise None.
        """
        if edge in self.edges:
            return edge

        for existing_edge in self.edges:
            if existing_edge.has_vertex(edge.v_from) and existing_edge.has_vertex(edge.v_to):
                return existing_edge

        return None

    def has_edge(self, edge: Edge) -> bool:
        """
        Checks whether the graph contains an edge.
        :param edge: The edge to be checked for.
        :return: True if the edge is found in the graph, otherwise False.
        """
        return edge in self.edges or self.find_edge(edge) is not None

    def add_edge(self, edge: Edge) -> None:
        """
        Adds an edge to the graph. If the edge's vertices are not yet part of the graph, they are added too.
        :param edge: The edge to be added.
        """
        if self.has_edge(edge) or edge.v_to == edge.v_from:
            return

        self._edges.append(edge)
        self._add_missing_vertices(edge)

    def delete_edge(self, edge: Edge) -> None:
        """
        Deletes an edge from the graph and removes the edge's vertices, that are not referenced by any other edge.
        :param edge: The edge to be removed.
        """
        edge_obj = self.find_edge(edge)

        if not edge_obj:
            return

        self._edges.remove(edge_obj)

        # Delete those vertices, that are not referenced by at least one other edge
        for vertex in (edge_obj.v_from, edge_obj.v_to):
            if not self.is_vertex_referenced(vertex):
                self.delete_vertex(vertex)

    def find_neighbours(self, vertex: Vertex) -> list[Vertex]:
        """
        Finds all vertices connected to the vertex with an edge.
        :param vertex: The vertex to be checked with.
        :return: A list of neighbours, or an empty list if there are none.
        """
        result = []

        for edge in self._edges:
            if edge.v_from == vertex:
                result.append(edge.v_to)
            elif edge.v_to == vertex:
                result.append(edge.v_from)

        return result

    def has_neighbours(self, vertex: Vertex) -> bool:
        """
        Checks whether the given vertex has any edges connecting it to other vertices.
        :param vertex: The vertex to be checked.
        :return: True if the vertex has any neighbours, otherwise False.
        """
        for edge in self._edges:
            if vertex in (edge.v_from, edge.v_to):
                return True

        return False

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
        return any(edge.has_vertex(vertex) for edge in self._edges)

    def set_all_visited(self, visited: bool) -> None:
        """
        Changes the `visited` value for every vertex in the graph.
        :param visited: The value to change the `visited` value to.
        """
        for vertex in self.vertices:
            vertex.visited = visited

    def all_visited(self, visited: bool) -> bool:
        """
        Checks if all vertices in the graph are visited.
        :param visited: Can be True to check if all vertices are visited, or False to check if none are visited.
        :return: True if all vertices' visited state match the `visited` parameter, otherwise False.
        """
        for vertex in self._vertices:
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
                result.append(self.find_edge(Edge(edge_from, edge_to)))

        return result

    def _add_missing_vertices(self, edge: Edge) -> None:
        for vertex in (edge.v_from, edge.v_to):
            if not self.has_vertex(vertex):
                self.add_vertex(vertex)
