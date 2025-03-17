import random

from noise import pnoise1
from src.generator.graph.vertex import Vertex


def bresenham_line(start_vertex: Vertex, end_vertex: Vertex) -> list[tuple[int, int]]:
    # TODO may be replaced with skimage.draw.line for performance.
    points = []

    start_x = start_vertex.x
    start_y = start_vertex.y
    end_x = end_vertex.x
    end_y = end_vertex.y

    delta_x = abs(end_x - start_x)
    delta_y = abs(end_y - start_y)
    step_x = 1 if start_x < end_x else -1
    step_y = 1 if start_y < end_y else -1
    error = delta_x - delta_y

    current_x, current_y = start_x, start_y

    while True:
        points.append((current_x, current_y))
        if current_x == end_x and current_y == end_y:
            break
        double_error = 2 * error
        if double_error > -delta_y:
            error -= delta_y
            current_x += step_x
        if double_error < delta_x:
            error += delta_x
            current_y += step_y

    return points


def generate_widths(amount: int, base_width: int = 4, variation: int = 3, frequency: float = 0.1) -> list[int]:
    offset = random.randint(0, 1000)  # random offset for perlin noise

    widths = [
        base_width + int(pnoise1((i + offset) * frequency) * variation)
        for i in range(amount)
    ]

    return [max(1, width) for width in widths]
