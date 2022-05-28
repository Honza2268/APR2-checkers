from enum import Enum, IntEnum
from abc import ABC, abstractmethod
from treelib import Node, Tree

WHITE_SPOTS = list((i)+1*(i//8 % 2) for i in range(0, 64, 2))


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


class Piece(ABC):
    def __init__(self, color: Color, position=None, board=None):
        self.color = color
        self.position: int = position
        self._board: list = board
        self._moves: list
        self._captured = False
        self._text_color = Color_code[self.color.name]

    @abstractmethod
    def get_moves_p1(self, pos, direction, n_pos, used):...
    
    @abstractmethod
    def get_moves_p1(self, pos, direction, n_pos, used):...

    def get_moves(self, pos=None, directions=None, used=None, strict=False):
        moves = []

        if not used:
            used = []

        if self._captured:
            return [('captured')]

        if pos == None:
            pos = self.position
            moves.append(('start', pos))

        if not directions:
            directions = self._moves
        if type(directions) != list:
            directions = [directions]

        for direction in directions:
            n_pos = pos + direction

            if not 63 > n_pos > 0 or (n_pos - direction) // 8 == n_pos // 8 or abs(n_pos % 8 - pos % 8) > 1:
                # pokud je pozice s offsetem kroku kladná, za přelomem desky nebo není na platném poli, pokračuj na další
                # tldr: detekuje a skipuje nelegální pozice
                continue

            if not self._board[n_pos] and n_pos not in used:
                # pokud není pozice s offsetem kroku zabraná, přidej si ji do možných kroků
                moves.append(self.get_moves_p1(pos, direction, n_pos, used))

            elif self._board[n_pos].color != self.color and n_pos not in used:
                # pokud je na pozici kroku nepřátelská figurka, zaber ji, pokud je za ní místo
                moves.append(self.get_moves_p2(pos, direction, n_pos, used))

        if strict:
            ...
            #TODO: odstranění neuplatnitelných tahů podle pravidel
        
        return moves

    def vis_moves(self):
        # stolen from stackoverflow (https://stackoverflow.com/questions/64713797/visualizing-parse-tree-nested-list-to-tree-in-python)
        lst = self.get_moves()
        root, *tail = lst
        tree = Tree()
        node = Node(root)
        tree.add_node(node)

        q = [[node, *tail]]
        while q:
            parent, *children = q.pop()
            for child in children:
                if isinstance(child, list):
                    head, *tail = child
                    node = tree.create_node(head, parent=parent)
                    q.append([node, *tail])
                else:
                    tree.create_node(child, parent=parent)
        tree.show()


class Man(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self._moves = Moves[self.color.name].value
        self._king_zone = King_zone[self.color.name].value

    def place_on(self, board, position):
        if not self.position:
            self._board = board
            self.position = position
            self._board[position] = self
            return True
        return False

    def __repr__(self):
        return self._text_color.value+'a '

    def get_moves_p1(self, pos, direction, n_pos, used):
        return [('move', direction, n_pos)]

    def get_moves_p2(self, pos, direction, n_pos, used):
        if n_pos+direction < 64 and not self._board[n_pos+direction] and n_pos not in used:
            sub_move = []
            sub_move.append(('take', direction, n_pos))
            sub_move.append(*self.get_moves(
                pos=n_pos, directions=direction))
            return sub_move


class King(Piece):
    def __init__(self, man: Man):
        super().__init__(man.color, man.position, man._board)
        self._moves = Moves.KING.value

    def __repr__(self):
        return self._text_color.value+'b '

    def get_moves_p1(self, pos, direction, n_pos, used):
        sub_move = []
        sub_move.append(('move', direction, n_pos))
        n_move = self.get_moves(
            pos=n_pos, directions=direction, used=used)
        if n_move:
            sub_move.append(*n_move)
        return sub_move

    def get_moves_p2(self, pos, direction, n_pos, used):
        if n_pos+direction < 64 and not self._board[n_pos+direction]:
            used += [n_pos, n_pos+direction]
            sub_move = []
            sub_move.append(('take', direction, n_pos))
            sub_move.append([('move', direction, n_pos+direction)])
            n_move = self.get_moves(
                pos=n_pos+direction, used=used)
            if n_move:
                sub_move[-1] += n_move
            return sub_move
