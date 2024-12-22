from dataclasses import dataclass


@dataclass
class Vertex:
    x: int
    y: int
    visited: bool = False
