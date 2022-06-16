from abc import ABC, abstractmethod
from treelib import Node, Tree
from constants import *
from utilities import *


class Piece(ABC):
    def __init__(self, color: Color, position=None, board=None):
        self.color = color
        self.position: int = position
        self._board: list = board
        self._moves: list
        self._captured = False
        self._text_color = Color_code[self.color.name]

    def count_near_enemies(self, position=None, vision_range=1):
        if position == None:
            position = self.position
            
        near_enemies = 0
        for direction in self._moves:
            for i in range(vision_range):
                test_position = position + direction * (i+1)
                if test_position in ILLEGAL_POSITIONS or abs(test_position % 8 - test_position-direction % 8) > 1:
                    break
                if self._board[test_position] and self._board[test_position].color != self.color:
                    near_enemies += 1
        return near_enemies


    def get_moves_common(self, position, directions, local_root, move_tree):
        if not move_tree:
            move_tree = Tree()

        if position == None:
            position = self.position

        if not local_root:
            debug_print(f'Standing @ {position}')
            local_root = f'start@{position}n{move_tree.size()}'
            move_tree.create_node(local_root, local_root,
                                  parent=None, data=('start', 0, position))

        if not directions:
            directions = self._moves
        if type(directions) != list:
            directions = [directions]

        return position, directions, local_root, move_tree
    
    @abstractmethod
    def get_moves_uncommon(self, position, directions, direction, local_root, move_tree):...
    
    def get_moves(self, position=None, directions=None, local_root=None, move_tree=None):

        position, directions, local_root, move_tree = self.get_moves_common(
            position, directions, local_root, move_tree)

        for direction in directions:

            self.get_moves_uncommon(position, directions, direction, local_root, move_tree)

        return move_tree


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
    
    def get_moves_uncommon(self, position, directions, direction, local_root, move_tree):
        test_position = position + direction
        next_position = position + 2*direction
        if test_position in LEGAL_POSITIONS:
            # pokud je pozice platná...
            if self._board[test_position] and self._board[test_position].color != self.color:
                # a pokud na pozici je nepřátelská figurka
                last_take = f'take@{test_position}n{move_tree.size()}'
                if next_position in LEGAL_POSITIONS:
                    if not self._board[next_position]:
                        # a pokud je i následující pozice volná, přidej tah do možných tahů
                        last_move = f'move@{test_position}n{move_tree.size()}'
                        move_tree.create_node(last_take, last_take, None, data=(
                            'take', direction, test_position))
                        move_tree.create_node(last_move, last_move, last_take, data=(
                            'move', direction, test_position))
            elif not self._board[test_position] and not self.count_near_enemies():
                # a v blízkosti nejsou nepřátelé, přidej tah do možných tahů
                last_move = f'move@{test_position}n{move_tree.size()}'
                move_tree.create_node(last_move, last_move, last_take, data=(
                    'move', direction, test_position))


class King(Piece):
    def __init__(self, man: Man):
        super().__init__(man.color, man.position, man._board)
        self._moves = Moves.KING.value

    def __repr__(self):
        return self._text_color.value+'b '

    def get_moves_uncommon(self, position, directions, direction, local_root, move_tree):
        contact = 0
        subtree = Tree()
        last_take = None
        last_move = None
        
        visible_enemies = self.count_near_enemies(position, 8)
        
        if visible_enemies:
            for test_position in range(position+direction, MAX_BOARD_INDEX+1 if direction > 0 else -1, direction):
                if test_position in ILLEGAL_POSITIONS:
                    # pokud je pozice neplatná, končím
                    break
                if contact:
                    # pokud došlo ke kontaktu s nepřátelskou figurkou, zkontroluj další pole pro doskok
                    if (self._board[test_position] or not
                            (MAX_BOARD_INDEX >= test_position >= 0)):
                        # pokud je na poli figrka, končime
                        debug_print(f'Bust @ {test_position}.')
                        break
                    else:
                        # pokud na poli není figurka, přidej tah do možných tahů
                        debug_print(
                            f'Found valid landing spot @ {test_position}, adding.')
                        last_move = f'move@{test_position}n{move_tree.size()+subtree.size()}'
                        subtree.create_node(last_move, last_move, last_take, data=(
                            'move', direction, test_position))

                        self.get_moves(position=test_position, directions=[
                                        x for x in self._moves if x != -direction], local_root=last_move, move_tree=subtree)

                elif self._board[test_position] and self._board[test_position].color != self.color:
                    # pokud najednou najdeš nepřátelskou figurku, nastav flag 'contact' na jeho pozici
                    contact = test_position

                    last_take = f'take@{test_position}n{move_tree.size()+subtree.size()}'
                    subtree.create_node(last_take, last_take, None, data=(
                        'take', direction, test_position))

                    debug_print(
                        f'Enemy @ {test_position}, checking for possible moves...')

            if len(subtree) > 1:
                # pokud jsou nějaké pohyby v připravované sekvenci, přidej ji do možných tahů
                move_tree.paste(local_root, subtree)
        else:
            # pokud nejsou žádné nepřátelské figurky v blízkosti, přidej tahy do možných tahů
            for test_position in range(position+direction, MAX_BOARD_INDEX+1 if direction > 0 else -1, direction):
                if test_position in ILLEGAL_POSITIONS:
                    # pokud je pozice neplatná, končíme
                    break 
                if not self._board[test_position]:
                    last_move = f'move@{test_position}n{move_tree.size()}'
                    move_tree.create_node(last_move, last_move, local_root, data=('move', direction, test_position))
                else:
                    # je na poli figurka, končíme
                    break

