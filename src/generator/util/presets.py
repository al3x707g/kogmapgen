from dataclasses import dataclass


@dataclass(frozen=True)
class Preset:
    border_width: int
    grid_width: int
    grid_height: int
    start_x: int
    start_y: int
    end_x: int
    end_y: int
    mesh_size: int
    min_width: int
    max_play: int


@dataclass(frozen=True)
class SimplePreset:
    border_width: int
    mesh_size: int
    mesh_spacing: int
    start: tuple[int, int]
    finish: tuple[int, int]
