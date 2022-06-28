from enum import Enum, IntEnum
from string import ascii_letters

#=====================DEBUG======================#
DEBUG_OUT = False

#===============Project=Constants================#
MAX_BOARD_INDEX = 63
BOARD_SIDE_LENGTH = 8

ILLEGAL_POSITIONS = list(x for x in range(64) if (x % 2) ^ (x // 8 % 2))
LEGAL_POSITIONS = list(x for x in range(64) if not (x % 2) ^ (x // 8 % 2))

DIRECTION_SYMBLOS = {7: '↖', 9: '↗', -9: '↙', -7: '↘'}

ESCAPE_CHAR = '[' #'\x1B['
#===============Utility=Constants================#


class Line_Types:
    class ascii_light:
        ...

    class ascii_heavy:
        ...

    class ascii_double:
        ...

    class ascii_curved:
        ...
    sets = {
        'ascii_light': {'horizontal': '─', 'vertical': '│', 'top_left': '┌', 'top_right': '┐', 'bottom_left': '└', 'bottom_right': '┘', 'vertical_left': '├', 'vertical_right': '┤', 'horizontal_down': '┬', 'horizontal_up': '┴', 'cross': '┼'},
        'ascii_heavy': {'horizontal': '━', 'vertical': '┃', 'top_left': '┏', 'top_right': '┓', 'bottom_left': '┗', 'bottom_right': '┛', 'vertical_left': '┣', 'vertical_right': '┫', 'horizontal_down': '┳', 'horizontal_up': '┻', 'cross': '╋'},
        'ascii_double': {'horizontal': '═', 'vertical': '║', 'top_left': '╔', 'top_right': '╗', 'bottom_left': '╚', 'bottom_right': '╝', 'vertical_left': '╠', 'vertical_right': '╣', 'horizontal_down': '╦', 'horizontal_up': '╩', 'cross': '╬'},
        'ascii_curved': {'horizontal': '─', 'vertical': '│', 'top_left': '╭', 'top_right': '╮', 'bottom_left': '╰', 'bottom_right': '╯', 'vertical_left': '├', 'vertical_right': '┤', 'horizontal_down': '┬', 'horizontal_up': '┴', 'cross': '┼'}
    }

    # found sets sopmewhere, didnt want to rewrite to class
    for set_name, set in sets.items():
        for name, shape in set.items():
            exec(f'{set_name}.{name} = "{shape}"')


ascii_light = Line_Types.ascii_light
ascii_heavy = Line_Types.ascii_heavy
ascii_double = Line_Types.ascii_double
ascii_curved = Line_Types.ascii_curved

#=====================Enums======================#


ascii_light = Line_Types.ascii_light
ascii_heavy = Line_Types.ascii_heavy
ascii_double = Line_Types.ascii_double
ascii_curved = Line_Types.ascii_curved

#=====================Enums======================#
class Color(IntEnum):
    BLACK = 0
    WHITE = 1

class Color_code(Enum):
    BLACK = f'{ESCAPE_CHAR}38;5;16m'
    WHITE = f'{ESCAPE_CHAR}38;5;15m'

class Moves(Enum):
    BLACK = [-9, -7]
    WHITE = [7, 9]
    KING = [7, 9, -9, -7]


class King_zone(Enum):
    BLACK = range(16)
    WHITE = range(48, 64)

class ALPHANUM(Enum):
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8
