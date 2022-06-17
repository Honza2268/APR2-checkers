from enum import Enum, IntEnum
from abc import ABC, abstractmethod
from turtle import position
from treelib import Tree

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
    
    def __init__(self, man):
        super().__init__(man.color, man.position, man._board)
        self._moves = Moves.KING.value    

    def get_moves(self, position=None, taken=[18]):
        moves = []        
        contact = False
        if self._taken: return moves
        if position == None:
            position = self.position
            moves.append(('start', position))
        for direction in self._moves:
            contact = False
            """cycle = self.cyklus_direction_loop(position,direction,moves,taken,contact)
            moves += cycle[0]
            taken += cycle[1]"""
            for new_position in (range(position+direction,64 if direction>0 else -1,direction)):
                if self.checking_new_postion(new_position,direction,taken):
                    break
                if not self._board[new_position]:
                    if position == self.position:
                        moves.append(('move', direction, new_position))
                    elif contact:
                        if new_position != self.position:
                            moves.append(('move', direction, new_position))
                    if contact:
                        taken.append(new_position)
                        move_repeat = self.get_moves(position=new_position,taken=taken)
                        if move_repeat != []:
                            moves.append((new_position,move_repeat))
                    contact = False
                elif self._board[new_position].color == self.color:
                    break
                elif self._board[new_position].color != self.color and new_position not in taken:
                    taken.append(new_position)
                    if contact == True:                    
                        break
                    contact = True
        
        return moves

    
    def checking_new_postion(self,new_position,direction,taken):
        if new_position<len(self._board) and new_position>=0: #kontrola jestli nová pozice figurky není mimo hrací desku
           print(new_position, "Prošlo první kontrolou")
           if (abs((new_position-direction)%self.number_of_rows - new_position % self.number_of_rows) == 1): #kontrola jestli předchozí pozice a nová pozci jsou sloupce vedle sebe               
                print(new_position, "prošlo druhou kontrolou")
                if new_position not in taken: #kontrola jestli nová pozice je už v možných tazích
                    print(new_position, "prošlo třetí kontrolou")
                    return False
        print(new_position,"neprošlo kontrolou")       
        return True
    
    def cyklus_direction_loop(self,position,direction,moves,taken,contact):        
        for new_position in range(position+direction,64 if direction>0 else -1,direction):
                if self.checking_new_postion(new_position,direction,taken):
                    break
                if not self._board[new_position]:
                    if position == self.position:
                        pass
                        moves.append(('move', direction, new_position))  
                    elif contact:
                        if new_position != self.position:
                            moves.append(('move', direction, new_position))
                    if contact:
                        taken.append(new_position)
                        move_repeat = self.get_moves(position=new_position,taken=taken)
                        if move_repeat != []:
                            moves.append((new_position,move_repeat))
                    contact = False
                elif self._board[new_position].color == self.color:
                    break
                elif new_position not in taken:
                    taken.append(new_position)
                    if contact == True:                    
                        break
                    contact = True
        return [moves,taken]   

        
    def __repr__(self):
        return self._text_color.value+'b '