import time

from src.generator.generator import Generator
from src.generator.map.map import Map
from src.generator.util.presets import SimplePreset

if __name__ == "__main__":
    start_time = time.perf_counter()
    preset: SimplePreset = SimplePreset(30, 30, 20, (0, 0), (29, 29))
    game_map: Map = Map(preset)

    gen: Generator = Generator(game_map)
    gen.generate_from_graph()

    game_map.save_image()
    end_time = time.perf_counter()
    print(f"generation took {end_time - start_time:.4f} seconds")
