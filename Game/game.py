from core import *
from player import *
from utilities import *
from constants import *
import random
from colorama import init
init()

def command_mode(game):
    clear_screen()
    print('Welcom to command mode!\nType `h` for aviable commands\n')
    commanding = True
    while commanding:
        command = input('> ')

        match command.split(' '):
            case ['h']:
                print('save: save current layout\nload: load layout from path\nsave_history: save current game as series of moves\nload_history: replay previously saved game\nrestart: start new game\nquit: exit the application\nclear: clear screen\ncontinue or `/`: retrun to game')
            case ['save']:
                print('Usage: save *file name*')
            case ['save', fn]:
                game.save(fn)
                print(f'File {fn} saved')
            case ['load']:
                print('Usage: load *file name*')
            case ['load', fn]:
                game.load_layout(fn)
                print(f'File {fn} loaded')
            case ['save_history']:
                game.save_history()
                print('File history.csv saved')
            case ['save_history', fn]:
                print(f'File {fn} saved')
                game.save_history(fn)
            case ['load_history']:
                print('File history.csv loaded')
                game.load_history()
            case ['load_history', fn]:
                print(f'File {fn} loaded')
                game.load_history(fn)
            case ['restart']:
                game.new_game()
                print('New game started')
            case ['quit']:
                exit()
            case ['clear']:
                clear_screen()
            case ['continue']|['/']:
                commanding = False
            case _:
                print('Invalid command')

def main():
    p1n = input('Player 1 name:\n> ')
    p2n = input('Player 2 name: (use `AUTO` to play against bot)\n> ')
    
    automatic = True if p2n == 'AUTO' else False
    
    player1 = Player(Color['WHITE'], p1n)
    player2 = Player(Color['BLACK'], p2n)
    
    g = Game((player1, player2))
    g.new_game()

    playing = True
    while playing:
        
        active_pieces = count(lambda x: g.get_piece_move_tree(x).size() > 1 and (not x._captured) and x.color == g.current_player.color, g.pieces)
        if active_pieces == 0:
            playing = False
            break
        else:
            for p in g.pieces:
                p._last_move_tree = None
                
        clear_screen()
        print(f'Player: {g.current_player.name} ({g.current_player.color.name})\n')
        g.print()
        
        print('Select piece (coordiantes eg.: a5), or type `/` for command mode:')
        
        selecting = True
        while selecting:
            piece = None
            selected_coordinates = input('> ').strip().casefold()
            
            if selected_coordinates.strip() == "/":
                command_mode(g)                
                break
            try:
                selected_position = g.anotation_to_position(selected_coordinates.strip())
            except:
                print('Invalid coordinates, try agin')
                continue
            
            match g.board[selected_position]:
                case None:
                    print('Empty space, try agin')
                case p if g.get_piece_move_tree(p).size() <= 1:
                    print('This piece cannot move, try agin')
                case piece if piece.color == g.current_player.color:
                    selecting = False
                case p if p.color != g.current_player.color:
                    print('Enemy piece, try agin')
        
        if piece == None:
            continue
        
        piece._last_move_tree = None
        moves = g.get_piece_moves(piece)
        move_tree = g.get_piece_move_tree(piece)
        move_visualization = []
        
        for i in range(len(moves)):
            steps = [move_tree.get_node(node).data for node in moves[i]]
            move_visualization.append(g.visualize_move(steps).split('\n'))
            move_visualization[i].insert(0, f'Move {i+1}:'.ljust(18))
        
        rotated_vis = [[move_visualization[j][i] for j in range(len(move_visualization))] for i in range(len(move_visualization[0])-1,-1,-1)]
        
        clear_screen()
        print('Aviable moves:')
        
        max_moves = 5
        multilne = (len(moves) // max_moves) +1
        
        for i in range(multilne):    
            finalmove = min(max_moves*(i+1), len(moves))
            for line in rotated_vis[::-1]:
                print('\t'.join(line[max_moves*i:finalmove]))
        
                
        
        print('Sellect move number, or `d` to sellect different piece:')
        selecting = True
        while selecting:
            selelected_move = input('> ').strip().casefold()
            if selelected_move == 'd':
                break
            try:
                selelected_move = int(selelected_move)
            except ValueError:
                print(f'{selelected_move} is not a number')
                continue
            selelected_move -= 1
            if not 0 <= selelected_move < len(moves):
                print('Invalid move number, try agin')
                continue
            else:
                selecting = False
                g.make_move(piece, selelected_move)            
        if selecting:
            continue
        
        if automatic:
            bot_piece_tree_size = 0
            while bot_piece_tree_size <= 1:
                bot_piece = random.choice(g.next_player.pieces)
                bot_piece_tree_size = g.get_piece_move_tree(bot_piece).size()
            yet_to_move = True
            bot_piece_moves = g.get_piece_moves(bot_piece)
            while yet_to_move:
                try:
                    bot_piece_move = random.randint(0, len(bot_piece_moves))
                    visual = g.make_move(bot_piece, bot_piece_move, True)
                    yet_to_move = False
                    clear_screen()
                    print('Bot made this move:\n')
                    print(visual)
                    input('(Press Enter to continue)')
                except AssertionError:
                    ...
            
        else:
            g.swap_active_players()
    
    clear_screen()
    print(f'Player {g.current_player.name} won!')
    save_q = input('Save replay? (y/n):\n> ')
    
    if save_q.strip().casefold() == 'y':
        fn = input('Enter file name (default is `history.csv`):\n> ')
        g.save_history(fn)
        

if __name__ == '__main__':
    main()