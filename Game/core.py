from player import Player
from pieces import Man, King
from constants import Color
from utilities import *


class Game:
    def __init__(self, players, starting_player=1):
        self.players = players
        self.current_player: Player
        self.next_player: Player

        self.board = [None] * 64
        self.pieces = []

    def new_game(self):
        self.board = [None] * 64
        self.pieces = []

        self.current_player = self.player[0]
        self.next_player = self.player[1]

        self.pieces = [Man(Color(i//8)) for i in range(16)]

        for i, p in enumerate(self.pieces):
            p.place_on(self.board, (i*2)+1*(i//4 % 2)+32*(i//8))

    def promote_piece(self, piece, force=False):
        if piece.position in piece._king_zone or force:
            k = King(piece)
            piece._board[piece.position] = k
            self.pieces[self.pieces.index(piece)] = k
            return True
        return False

    def print_numbers(self): print(self.__str__(numbers=True))
    def print(self): print(self.__str__())
    def d_print(self): print(self.__str__(numbers=True))

    def __str__(self, reverse=True, markings=True, numbers=False):
        c = [
            f'\x1B[48;5;{"142" if (p%2)^(p//8%2) else "64"}m{self.board[p] if self.board[p] and not self.board[p]._captured else "  " if not numbers else f"{p:02}"}\x1B[0m'
            for p in range(64)]
        l = [f'{(x+1) if markings else ""} '+''.join(c[x*8:x*8+8])
             for x in range(8)]
        return '\n'.join((['  A B C D E F G H'] if markings else []) + l[:: -1 if reverse else 1])

    def position_to_anotation(self, position):
        nta = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
        col = nta[position % 8+1]
        row = str((position//8)+1)
        return col+row

    def anotation_to_position(self, anotation):
        atn = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        col = atn[anotation[0]]-1
        row = int(anotation[1])-1
        return row*8+col

    def save(self, filename):
        data = {self.position_to_anotation(p.position): (
            'w' if p.color else 'b') * (1 if type(p) == Man else 2) for p in self.pieces}
        save_dict_csv(data, filename)

    def load_layout(self, filename):
        self.board = [None] * 64
        self.pieces = []

        data = load_dict_csv(filename)
        for anotation, piece in data.items():
            position = self.anotation_to_position(anotation)
            p = Man(Color(0 if 'b' in piece else 1))
            self.pieces.append(p)
            p.place_on(self.board, position)
            if len(piece) == 2:
                self.promote_piece(p, True)

    def get_piece_moves(self, piece):
        tree = piece.get_moves()

        paths = tree.paths_to_leaves()

        return paths

    def make_move(self, piece, move_id):
        piece.vis_moves()
        #TODO: this


if __name__ == "__main__":
    g = Game((Player(Color(0)), Player(Color(1))))
    try:
        g.load_layout('../test2.csv')
    except:
        g.load_layout('test2.csv')
    g.d_print()
    #g.make_move(g.pieces[0], 0)
    '''for l in g.get_piece_moves(g.pieces[0]):
        print(l)'''
    print(g.get_piece_moves(g.pieces[0]))
    print(g.pieces[0].get_moves())
