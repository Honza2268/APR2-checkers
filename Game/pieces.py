from abc import ABC, abstractmethod
from uuid import uuid1
from treelib import Tree
from constants import *
from utilities import *


class Piece(ABC):
    def __init__(self, color: Color, position: int = None, board: list = None):
        self.color = color
        self.position: int = position
        self._board: list = board
        self._moves: list
        self._captured = False
        self._text_color = Color_code[self.color.name]
        self._last_move_tree = None

    def count_near_enemies(self, position: int = None, vision_range: int = 1):
        if position == None:
            position = self.position

        near_enemies = 0
        for direction in self._moves:
            for i in range(vision_range):
                test_position = position + direction * (i+1)
                if test_position in ILLEGAL_POSITIONS or abs(test_position % 8 - (test_position-direction) % 8) > 1 or test_position > MAX_BOARD_INDEX:
                    break
                if self._board[test_position] and self._board[test_position].color != self.color:
                    near_enemies += 1
        return near_enemies

    def get_moves_common(self, position: int, used: list, local_root: str, move_tree: Tree):
        if move_tree is None:
            move_tree = Tree()

        if position == None:
            position = self.position

        if used is None:
            used = []

        if local_root is None:
            debug_print(f'Standing @ {position}')
            #local_root = f'start @ {position} node {move_tree.size()}'
            local_root_tag = f'{position}'
            local_root = str(uuid1())
            move_tree.create_node(local_root_tag, local_root,
                                  parent=None, data=('start', 0, position))

        return position, used, local_root, move_tree

    @abstractmethod
    def get_moves_uncommon(self, position: int, direction: int,
                           local_root: str, move_tree: Tree, used: list): ...

    def get_moves(self, position: int = None, used: list = None, local_root: str = None, move_tree: Tree = None, blocked = False):

        directions = self._moves

        position, used, local_root, move_tree = self.get_moves_common(
            position, used, local_root, move_tree)

        for direction in directions:

            self.get_moves_uncommon(
                position, direction, local_root, move_tree, used.copy(), blocked)
            
        if len(move_tree) == 1 and not blocked:
                move_tree = self.get_moves(None, None, None, None, True)

        self._last_move_tree = move_tree
        return move_tree


class Man(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self._moves = Moves[self.color.name].value
        self._king_zone = King_zone[self.color.name].value

    def place_on(self, board: list, position: int):
        if self.position is None:
            self._board = board
            self.position = position
            self._board[position] = self
            return True
        return False

    def __repr__(self):
        return self._text_color.value+'a ' if self._captured is False else '  '

    def get_moves_uncommon(self, position: int, direction: int, local_root: str, move_tree: Tree, used: list, blocked: bool):
        test_position = position + direction
        next_position = position + 2*direction
        if test_position in LEGAL_POSITIONS:
            # pokud je pozice platná...
            if self._board[test_position] and self._board[test_position].color != self.color:
                # a pokud na pozici je nepřátelská figurka
                last_take_tag = f'{test_position}{DIRECTION_SYMBLOS[direction]}'
                last_take = str(uuid1())
                
                if next_position in LEGAL_POSITIONS:
                    if self._board[next_position] is None:
                        # a pokud je i následující pozice volná, přidej tah do možných tahů

                        last_move_tag = f'{next_position}{DIRECTION_SYMBLOS[direction]}'
                        last_move = str(uuid1())
                        move_tree.create_node(last_take_tag, last_take, local_root, data=(
                            'take', direction, test_position))
                        move_tree.create_node(last_move_tag, last_move, last_take, data=(
                            'move', direction, test_position))

            elif self._board[test_position] is None and (self.count_near_enemies() == 0 or blocked):
                # a v blízkosti nejsou nepřátelé, přidej tah do možných tahů
                last_move_tag = f'{test_position}{DIRECTION_SYMBLOS[direction]}'
                last_move = str(uuid1())
                move_tree.create_node(last_move_tag, last_move, local_root, data=(
                    'move', direction, test_position))


class King(Piece):
    def __init__(self, man: Man):
        super().__init__(man.color, man.position, man._board)
        self._moves = Moves['KING'].value

    def __repr__(self):
        return self._text_color.value+'b ' if self._captured is False else '  '

    def get_moves_uncommon(self, position: int, direction: int, local_root: str, move_tree: Tree, used: list, blocked: bool):
        contact = None
        subtree = Tree()

        visible_enemies = self.count_near_enemies(self.position, 8)

        if visible_enemies and not blocked:
            for test_position in range(position + direction, MAX_BOARD_INDEX+1 if direction > 0 else -1, direction):
                move_tag = f'{test_position}{DIRECTION_SYMBLOS[direction]}'
                if test_position in ILLEGAL_POSITIONS:
                    # pokud je pozice neplatná, končím
                    break

                if contact:
                    # pokud došlo ke kontaktu s nepřátelskou figurkou, zkontroluj další pole pro doskok
                    if self._board[test_position]:
                        # pokud je na poli figrka, končime
                        debug_print(f'Bust @ {test_position}.')
                        break
                    else:
                        # pokud na poli není figurka, přidej tah do možných tahů
                        #last_move = f'move @ {test_position} going {DIRECTION_SYMBLOS[direction]} node {move_tree.size()+subtree.size()}'
                        last_move = str(uuid1())
                        used.append(contact)
                        subtree.create_node(move_tag, last_move, last_take, 
                                            data=('move', direction, test_position))
                        
                        debug_print(
                            f'Found valid landing spot @ {test_position}, adding.')

                        self.get_moves(position=test_position, used=used.copy(
                        ), local_root=last_move, move_tree=subtree, blocked=blocked)

                elif self._board[test_position] and self._board[test_position].color != self.color and test_position not in used:
                    # test_position není None & na poli je nepřátelská figurka & ještě nebyla použita
                    # pokud najdeš nepřátelskou figurku, nastav 'contact' na její pozici
                    contact = test_position                
                    #last_take_tag = f'{test_position}{DIRECTION_SYMBLOS[direction]}'
                    last_take = str(uuid1())
                    
                    subtree.create_node(move_tag, last_take, None,
                                        data=('take', direction, test_position))

                    debug_print(
                        f'Enemy @ {test_position}, checking for landing spots...')

            if len(subtree) > 1:
                # pokud jsou nějaké pohyby v připravované sekvenci, přidej ji do možných tahů

                move_tree.paste(local_root, subtree)
                

        else:
            # pokud nejsou žádné nepřátelské figurky v blízkosti, přidej tahy do možných tahů
            for test_position in range(position+direction, MAX_BOARD_INDEX+1 if direction > 0 else -1, direction):
                move_tag = f'{test_position}{DIRECTION_SYMBLOS[direction]}'
                if test_position in ILLEGAL_POSITIONS:
                    # pokud je pozice neplatná, končíme
                    break
                if self._board[test_position] is None:
                    last_move = str(uuid1())
                    
                    move_tree.create_node(move_tag, last_move, local_root,
                                          data=('move', direction, test_position))
                else:
                    # je na poli figurka, končíme
                    break