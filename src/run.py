from src.generator.generator import Generator
from src.generator.map.map import Map
from src.generator.util.presets import SimplePreset

if __name__ == "__main__":
    preset: SimplePreset = SimplePreset(10, 30, 30, (0, 0), (29, 29))
    game_map: Map = Map(preset)

    gen: Generator = Generator(game_map)
    gen.generate_from_graph()

    gen.paint_all_vertices()
    gen.paint_all_edges()

    game_map.save_image()
