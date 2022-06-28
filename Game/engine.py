from constants import *
from typing import *


class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.directions = Directions(self)
        self.annotation = Annotation(self)
        self.content = [None for _ in range(self.width * self.height)]

    def _normalize_position(self, position: int | tuple[int, int] | str):
        match position:
            case p if type(p) == int:
                if not 0 <= p < len(self.content):
                    raise IndexError('Position is out of bounds')

            case (x, y) if type(x) == type(y) == int:
                if not 0 <= x < self.width and 0 <= y < self.height:
                    raise IndexError('Position is out of bounds')
                p = y*self.width+x

            case a if self.annotation.is_thing_annotation(a):
                p = self.annotation >> a

            case _:
                raise TypeError('Invalid input')

        return p

    def _get_column(self, position: int):
        return position % self.width

    def _get_row(self, position: int):
        return position // self.width

    def get_content_on(self, position: int | tuple[int, int]):
        p = self._normalize_position(position)
        return self.content[p]

    def set_content_on(self, object, position: int | tuple[int, int]):
        p = self._normalize_position(position)
        self.content[p] = object


class Directions:
    def __init__(self, board: Board):
        self.board = board

        self.LEFT = -1
        self.RIGHT = -self.LEFT
        self.UP = self.board.width
        self.DOWN = -self.UP
        self.UPRUGHT = self.UP + self.RIGHT
        self.DOWNLEFT = self.DOWN + self.LEFT
        self.DOWNRIGHT = self.DOWN + self.RIGHT


class Annotation:
    def __init__(self, board: Board):
        self.board = board

    def __lshift__(self, other: int | tuple[int, int]):
        # numer / tuple to annotation
        p = self.board._normalize_position(other)
        column = self.board._get_column(p) + 1
        row = self.board._get_row(p) + 1

        letters = []
        
        while column:
            letters.append(chr(96 + column % 26))
            column //= 26

        return f'{"".join(letters[::-1])}{row}'

    def __rshift__(self, other: str):
        # anotation to number
        column = 0
        row = 0

        letters = []

        for i, ch in enumerate(other):
            if ch.isnumeric():
                row = int(other[i:]) - 1
                break
            letters.append(ch)

        for i, l in enumerate(letters):
            column += i * 26 + ord(l) - 97

        if column > self.board.width or row > self.board.height:
            raise ValueError('Annotation cannot be applied to board')

        return self.board._normalize_position((column, row))

    def is_thing_annotation(self, thing):
        try:
            self >> thing
            return True
        except ValueError:
            return False


class Move:
    def __init__(self, direction: Directions, start_position: int, distance=1):
        self.direction = direction
        self.start_position = start_position
        self.distance = distance
        self.end_position = start_position + distance * direction


if __name__ == '__main__':
    b = Board(8, 8)
    a = b.annotation << (29, 0)
    print(a)
    print(b.annotation >> a)
    b.annotation.is_thing_annotation('a4')
