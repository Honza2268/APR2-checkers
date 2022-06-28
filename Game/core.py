from player import Player
from pieces import Man, King, Piece
from constants import *
from utilities import *


class Game:
    def __init__(self, players: tuple[Player, Player]):
        self.players = players
        self.current_player: Player
        self.next_player: Player

        self.board = [None] * 64
        self.pieces = []
        self.history = []

    def new_game(self):
        self.board = [None] * 64
        self.pieces = []

        self.current_player = self.players[0]
        self.next_player = self.players[1]

        self.pieces = [Man(Color(i//8)) for i in range(16)]

        for i, p in enumerate(self.pieces):
            p.place_on(self.board, (i*2)+1*(i//4 % 2)+32*(i//8))

    def swap_active_players(self):
        self.current_player, self.next_player = self.next_player, self.current_player

    def promote_piece(self, piece, force=False):
        if piece.position in piece._king_zone or force:
            k = King(piece)
            piece._board[piece.position] = k
            self.pieces[self.pieces.index(piece)] = k
            return True
        return False

    def print_numbers(self): print(self.__str__(numbers=True))
    def print(self): print(self.__str__())
    def debug_print(self): print(self.__str__(numbers=True))

    def __str__(self, reverse=True, markings=True, numbers=False, payload=None):
        if not payload:
            payload = self.board
        columns = [
            f'\x1B[48;5;{"142" if (p%2)^(p//8%2) else "64"}m{payload[p] if payload[p] else "  " if not numbers else f"{p:02}"}\x1B[0m'
            for p in range(64)]
        lines = [f'{(x+1) if markings else ""} '+''.join(columns[x*8:x*8+8])
                 for x in range(8)]
        return '\n'.join((['  A B C D E F G H'] if markings else []) + lines[:: -1 if reverse else 1])

    def position_to_anotation(self, position):
        column = ALPHANUM(position % 8 + 1).name
        row = str((position//8)+1)
        return column+row

    def anotation_to_position(self, anotation):
        column = ALPHANUM[anotation[0]].value-1
        row = int(anotation[1])-1
        return row*8+column

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

    def get_piece_moves(self, piece: int | Piece):
        if type(piece) == int:
            assert piece < len(self.pieces), 'Invalid piece index'
            piece = self.pieces[piece]

        tree = piece._last_move_tree if piece._last_move_tree else piece.get_moves()

        paths = tree.paths_to_leaves()

        return paths

    def get_piece_move_tree(self, piece: int | Piece):
        if type(piece) == int:
            assert piece < len(self.pieces), 'Invalid piece index'
            piece = self.pieces[piece]

        return piece._last_move_tree if piece._last_move_tree else piece.get_moves()

    def make_move(self, piece: int | Piece, move_id: int, visualize=False):
        if type(piece) == int:
            assert piece < len(self.pieces), 'Invalid piece index'
            piece = self.pieces[piece]

        moves = self.get_piece_moves(piece)
        move_tree = self.get_piece_move_tree(piece)
        assert move_id < len(moves), 'Invalid move id'

        steps = [move_tree.get_node(node).data for node in moves[move_id]]

        if visualize:
            print(self.visualize_move(steps))

        self.add_to_history(piece,steps)
        for command, direction, position in steps:
            match command:
                case 'start':
                    ...
                case 'move':
                    self.board[position], self.board[piece.position] = piece, None
                    piece.position = position
                case 'take':
                    self.board[position]._captured = True
        piece._last_move_tree = None
        return True
    
    def add_to_history(self,piece, steps):
        self.history.append((piece.position,steps))
    
    def save_history(self,filename='history.csv'):
        history = {i: self.history[i] for i in range(len(self.history))}
        save_dict_csv(history,filename)

    def visualize_move(self, steps: list, reverse=True, markings=True, numbers=False):
        visual = self.board.copy()

        last_command = None
        last_position = None

        for command, direction, position in steps:
            match command:
                case 'start':
                    visual[position] = visual[position].__str__(
                    ).strip()+'\x1B[1m\x1B[38;5;1mO\x1B[22m'
                case 'move':
                    visual[position] = '\x1B[1m\x1B[38;5;1m O\x1B[22m'
                case 'take':
                    visual[position] = visual[position].__str__().strip(
                    )+f'\x1B[1m\x1B[38;5;1m{DIRECTION_SYMBLOS[direction]}\x1B[22m'
            last_command = command
            if last_command in ('move', 'take') and abs(position-last_position) % 8 > 1:
                for inbetween_position in range(last_position+direction, position, direction):
                    visual[inbetween_position] = f'\x1B[1m\x1B[38;5;1m {DIRECTION_SYMBLOS[direction]}\x1B[22m'
            last_position = position

        return self.__str__(reverse=reverse, markings=markings, numbers=numbers, payload=visual)

if __name__ == "__main__":
    g = Game((Player(Color(0)), Player(Color(1))))

    layout = 'test_multi_take'

    try:
        g.load_layout(f'layouts/{layout}.csv')
    except:
        g.load_layout(f'Game/layouts/{layout}.csv')

    for i in range(len(g.get_piece_moves(0))):
        try:
            g.load_layout(f'layouts/{layout}.csv')
        except:
            g.load_layout(f'Game/layouts/{layout}.csv')
        g.make_move(0, i, True)
    #g.debug_print()

    '''for i in range(len(g.get_piece_moves(0))):
        try:
            g.load_layout(f'layouts/{layout}.csv')
        except:
            g.load_layout(f'Game/layouts/{layout}.csv')
        g.make_move(0, i, True)'''
    # g.debug_print()

    #print('\nTree:\n' + str(g.get_piece_move_tree(0)))
    #print('\nTree:\n' + str(g.get_piece_move_tree(5)))
    #print('\nMoves:\n')
    '''for m in g.get_piece_moves(0):
        print(m)'''
    g.make_move(0,2)
    g.print()
