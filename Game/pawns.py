from enum import Enum, IntEnum
from abc import ABC, abstractmethod

class Color(IntEnum):
    BLACK = 0
    WHITE = 1
  

class Color_code(Enum):
    BLACK = '\x1B[38;5;16m'
    WHITE = '\x1B[38;5;15m'
    
    
class Moves(Enum):
    BLACK = [7, 9]
    WHITE = [-9, -7]
    KING = [v*i for i in range(1, 8) for v in (7, 9, -9, -7)]
    

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
            
    def get_moves(self, pos=None, taken=[]):
        moves = []
        
        if self._taken: return moves
        
        if not pos:
            pos = self.position
            moves.append(('start', pos))
        
        for move in self._moves:
            try:
                if pos + move < 0 or pos + move not in ((i)+1*(i//8%2) for i in range(0, 64, 2)) or abs((pos + move) % 8 - pos % 8) != self._moves.index(move)//4+1:
                    # pokud je pozice s offsetem kroku kladná, za přelomem desky nebo není na platném poli, pokračuj na další
                    continue
                
                if not self._board[pos + move]:
                    # pokud není pozice s offsetem kroku zabraná, přidej si ji do možných kroků
                    moves.append(('move', move, pos + move))
                    
                elif self._board[pos + move].color != self.color:
                    ... # TODO: zabírání
            except IndexError: pass
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
    def __init__(self, man: Man):
        super().__init__(man.color, man.position, man._board)
        self._moves = Moves.KING.value
    
    def __repr__(self):
        return self._text_color.value+'b '