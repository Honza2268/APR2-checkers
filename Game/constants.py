from enum import Enum, IntEnum

DEBUG_OUT = False

MAX_BOARD_INDEX = 63
BOARD_SIDE_LENGTH = 8

ILLEGAL_POSITIONS = list(x for x in range(64) if (x % 2) ^ (x // 8 % 2))
LEGAL_POSITIONS = list(x for x in range(64) if not (x % 2) ^ (x // 8 % 2))


class Color(IntEnum):
    BLACK = 0
    WHITE = 1


class Color_code(Enum):
    BLACK = '\x1B[38;5;16m'
    WHITE = '\x1B[38;5;15m'


class Moves(Enum):
    BLACK = [7, 9]
    WHITE = [-9, -7]
    KING = [7, 9, -9, -7]  # [v*i for i in range(1, 8) for v in (7, 9, -9, -7)]


class King_zone(Enum):
    BLACK = range(48, 64)
    WHITE = range(16)
