from enum import Enum, IntEnum
from abc import ABC, abstractmethod
from turtle import pos

from numpy import true_divide

WHITE_SPOTS = list((i)+1*(i//8%2) for i in range(0, 64, 2))
class Color(IntEnum):
    BLACK = 0
    WHITE = 1
  

class Color_code(Enum):
    BLACK = '\x1B[38;5;16m'
    WHITE = '\x1B[38;5;15m'
    
    
class Moves(Enum):
    BLACK = [7, 9]
    WHITE = [-9, -7]
    KING = [7, 9, -9, -7]  #[v*i for i in range(1, 8) for v in (7, 9, -9, -7)]
    

class King_zone(Enum):
    BLACK = range(48,64)
    WHITE = range(16)


class Piece(ABC):
    @abstractmethod
    def __init__(self, color: Color, position = None, board = None):
        self.color = color
        self.position: int = position
        self._board: list = board
        self._moves: list
        self._taken = False
        self._text_color = Color_code[self.color.name]
            
    def get_moves(self, pos=None, directions=None):
        moves = []

        if self._taken: return moves

        if not pos:
            pos = self.position
            moves.append(('start', pos))

        if not directions:
            directions = self._moves
        if type(directions) != list:
            directions = [directions]

        for move in directions:
            n_pos = pos + move
            try:

                if n_pos < 0 or n_pos not in WHITE_SPOTS or abs((n_pos) % 8 - pos % 8) > 1:
                    # pokud je pozice s offsetem kroku kladná, za přelomem desky nebo není na platném poli, pokračuj na další
                    #tldr: detekuje a skipuje nelegální pozice
                    print('skipping')
                    continue

                if not self._board[n_pos]:
                    # pokud není pozice s offsetem kroku zabraná, přidej si ji do možných kroků
                    moves.append(('move', move, n_pos))

                elif self._board[n_pos].color != self.color:
                    # pokud je na pozici kroku nepřátelká figurrka, zaber ji
                    sub_move = []
                    sub_move.append(('take', move, n_pos))
                    sub_move.append(*self.get_moves(pos=pos+move, directions=move))
                    moves.append(sub_move)

            except IndexError: print('endexErr')
        return moves
        
        
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
    
    
class King(Piece):
    
    number_of_rows = 8
    
    def __init__(self, man: Man):
        super().__init__(man.color, man.position, man._board)
        self._moves = Moves.KING.value    
    
    def get_moves(self, position=None, directions=None):
        move_list = []
        if not directions:
            directions = self._moves
       
        if not position:
            position = self.position            
        
        for direction in directions:
            new_position = position+direction 
            while new_position<64 and new_position>-1:
                if direction<0:
                    print(new_position, "Direction je menší jak 0")
                    new_position += direction
                else:
                    print(new_position,"direction je větši jak 0")
                    if abs(new_position % 8 - position%8) == 1:
                        print(new_position, "prošlo to podmínkou")
                        if not self._board[new_position]:
                            print(new_position, "políčko je prázdný")
                            move_list.append(f"OLD: {position}  NEW:  {new_position}")
                            new_position += direction
                            
        return move_list
    def __repr__(self):
        return self._text_color.value+'b '
                            
                        
                    
                    
    