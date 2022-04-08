altonum = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
numtoal = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i'}

class MOVES:
    UP = [7, 9]
    DOWN = [-7, -9]
    KING = [7, 9, -7, -9]

    
class Piece: #☁
    
    def __init__(self, board, player, pos):
        self._king = False
        self._taken = False
        self._board = board
        self._side = player
        self._moves = MOVES.UP if self._side == self._board._player1 else MOVES.DOWN
        self._goal = range(8) if self._moves == MOVES.DOWN else range(56, 64)
        self._pos = pos

    def get_plays(self, pos=None, claimed=None):
        '''Check all possible plays for this piece.\n
        Retruns list of possible moves and claims.'''
        moves = []
        claims = []
        if not claimed:
            claimed=[]
        if self._taken:
            return moves, claims
        
        if not pos:
            pos = self._pos
            
        for m in self._moves:
            try:
                # TODO: dáma se může hýbat
                if abs((pos+m)%8-pos%8) != 1:
                    continue
                if not self._board._board[pos+m]:
                    moves.append(pos+m)
                elif self._board._board[pos+m]._side != self._side and not self._board._board[pos+2*m] and pos+m not in claimed and abs(pos%8-(pos+2*m)%8) <= 2:
                    claimed.append(pos+m)
                    cur_claim = pos+2*m
                    claims.append([pos+m, cur_claim])
                    _, next_claims = self.get_plays(cur_claim, claimed)
                    if next_claims:
                        for nc in next_claims:
                            claims.append([pos+m, cur_claim] + (nc if type(nc)==list else [nc]))
            except IndexError:
                pass
            
        return moves, claims
        
    def try_make_king(self):
        if self._pos in self._goal and not self._king:
            self._king = True
            self._moves = MOVES.KING
            return True
        return False
            
    def __repr__(self):
        return f'{self._side._color}{"⦿ "if not self._king else "t "}'
    
    
class Board: #☁
    
    def __init__(self, players, rows=2, save=None):
        '''Initialize the game with list of 2 players with different sides and number of rows (1-3) of game pieces'''
        
        assert 1 <= rows <= 3, 'Amount of rows needs to be 1, 2 or 3.'
        
        self._player1, self._player2 = players
        self._player1._board = self
        self._player2._board = self
        
        #TODO: test saving and loading
        if not save:
            self._board = [None for _ in range(8*8)]
            
            for p in range(0, 8*8, 2):
                side = self._player1 if p < (8*4) else self._player2
                if p in range(0, rows*8) or p in range(64-rows*8, 64):
                    piece = Piece(self, side, p+(p//8%2))
                    self._board[p+(p//8%2)] = piece
                    side._pieces.append(piece)
        else:
            self._board = save['board']
            self._player1 = save['p1']
            self._player2 = save['p2']
       
    def print(self, reverse=True, markings=True, numbers=False): print(self.__repr__(reverse, markings, numbers))
    def __repr__(self, reverse=True, markings=True, numbers=False):
        c = []
        l = []
        
        for p in range(64):          
            c.append(f'\x1B[48;5;{"142" if (p%2)^(p//8%2) else "64"}m{self._board[p] if self._board[p] and not self._board[p]._taken else "  " if not numbers else f"{p:02}"}\x1B[0m')
        for x in range(8):
            l.append(f'{(x+1) if markings else ""} '+''.join(c[x*8:x*8+8]))
        return '\n'.join((['  A B C D E F G H'] if markings else []) + l[:: -1 if reverse else 1])
            

class Player: #☁
    
    def __init__(self, name, first=False): 
        self._first = first
        self._color = '\x1B[38;5;15m' if self._first else '\x1B[38;5;16m'
        self._name = name
        self._board = None
        self._pieces = []

    def play(self, piece, route):
        if type(piece) == int:
            piece = self._pieces[piece]
        p, t = piece.get_plays()
        
        if p or t:
            routes = p if not t else t
            input((p, t))
            steps = routes[route]
            
            if type(steps) != list:
                steps = [steps]
            
            for step in steps:
                if (b := self._board._board[step]):
                    b._taken = True
                    b = None
                    
            self._board._board[piece._pos] = None
            self._board._board[steps[-1]] = piece
            piece._pos = steps[-1]
            
            piece.try_make_king()
        
    def visualize_play(self, piece, route):
        board = self._board.__repr__()
        p, t = piece.get_plays()
        
        routes = p if not t else t
        steps = routes[route]
        
        if len(steps) == 1:
            return
        
        pos = self._pos
        for step in steps:
            ...
    
    def get_valid_plays(self):
        plays = {}
        
        for i, piece in enumerate(self._pieces):
            p, t = piece.get_plays()
            if p or t:
                plays[i] = p if not t else t
        return plays


if __name__ == '__main__':
    p1, p2 = Player('1', True), Player('2')
    b = Board((p1, p2), 2)
    b.print(numbers=True)