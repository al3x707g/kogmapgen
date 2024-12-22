from dataclasses import dataclass


@dataclass(frozen=True)
class Preset:
    grid_size: int
    start_x: int
    start_y: int
    end_x: int
    end_y: int
    mesh_size: int
    min_width: int
    max_play: int
