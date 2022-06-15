from abc import ABC, abstractmethod
from treelib import Node, Tree
from constants import *


class Piece(ABC):
    def __init__(self, color: Color, position=None, board=None):
        self.color = color
        self.position: int = position
        self._board: list = board
        self._moves: list
        self._captured = False
        self._text_color = Color_code[self.color.name]

    @abstractmethod
    def get_moves_p1(self, position, direction, new_position, used): ...

    @abstractmethod
    def get_moves_p1(self, position, direction, new_position, used): ...

    def get_moves(self, position=None, directions=None, used=None):
        moves = []

        if not used:
            used = []

        if self._captured:
            return [('captured')]

        if position == None:
            position = self.position
            moves.append(('start', 0, position))

        if not directions:
            directions = self._moves
        if type(directions) != list:
            directions = [directions]

        for direction in directions:
            new_position = position + direction

            if (not MAX_BOARD_INDEX > new_position >= 0) or (new_position - direction) // BOARD_SIDE_LENGTH == new_position // BOARD_SIDE_LENGTH or abs(new_position % BOARD_SIDE_LENGTH - position % BOARD_SIDE_LENGTH) > 1:
                # pokud je pozice s offsetem kroku kladná, za přelomem desky nebo není na platném poli, pokračuj na další
                # tldr: detekuje a skipuje nelegální pozice
                continue

            if not self._board[new_position] and new_position not in used:
                # pokud není pozice s offsetem kroku zabraná, přidej si ji do možných kroků
                moves.append(self.get_moves_p1(
                    position, direction, new_position, used, moves))

            elif self._board[new_position].color != self.color and new_position not in used:
                # pokud je na pozici kroku nepřátelská figurka, zaber ji, pokud je za ní místo
                moves.append(self.get_moves_p2(
                    position, direction, new_position, used, moves))

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

    def get_moves_p1(self, position, direction, new_position, used, moves):
        return [('move', direction, new_position)]

    def get_moves_p2(self, position, direction, new_position, used, moves):
        if new_position+direction <= MAX_BOARD_INDEX and not self._board[new_position+direction] and new_position not in used:
            sub_move = []
            sub_move.append(('take', direction, new_position))
            sub_move.append(*self.get_moves(
                position = new_position, directions=direction))
            return sub_move


class King(Piece):
    def __init__(self, man: Man):
        super().__init__(man.color, man.position, man._board)
        self._moves = Moves.KING.value

    def __repr__(self):
        return self._text_color.value+'b '

    def get_moves_p1(self, position, direction, new_position, used, moves):
        sub_move = []
        sub_move.append(('move', direction, new_position))
        next_move = self.get_moves(
            position=new_position, directions=direction, used=used)
        if next_move:
            sub_move.append(*next_move)
        return sub_move

    def get_moves_p2(self, position, direction, new_position, used, moves):
        if new_position+direction <= MAX_BOARD_INDEX and not self._board[new_position+direction]:
            used += [new_position, new_position+direction]
            sub_move = []
            sub_move.append(('take', direction, new_position))
            sub_move.append([('move', direction, new_position+direction)])
            next_move = self.get_moves(
                position=new_position+direction, used=used)
            if next_move and any('take' in i[0] for i in next_move):
                sub_move[-1] += next_move
            return sub_move
