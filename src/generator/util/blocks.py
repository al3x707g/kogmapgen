from enum import Enum


class BlockType(Enum):
    EMPTY = 0
    HOOKABLE = 1
    FREEZE = 9
    SPAWN = 192
    START = 33
    FINISH = 34
    FLOOD = 999


class BlockColor:
    DEFAULT_COLOR = "#d3d3d3"

    colors: dict[BlockType, str] = {
        BlockType.EMPTY: DEFAULT_COLOR,
        BlockType.HOOKABLE: "#a9a9a9",
        BlockType.FREEZE: "#898989",
        BlockType.SPAWN: "#ffffff",
        BlockType.START: "#00ff00",
        BlockType.FINISH: "#ffa500",
        BlockType.FLOOD: "#ff0000"
    }

    @staticmethod
    def get(block_type: BlockType) -> str:
        return BlockColor.colors.get(block_type, BlockColor.DEFAULT_COLOR)
