from core import *
from player import *
from utilities import *
from constants import *


def main():
    p1n = input('Player 1 name:\n')
    p2n = input('Player 2 name:\n')

    player1 = Player(Color['WHITE'], p1n)
    player2 = Player(Color['BLACK'], p2n)

    g = Game((player1, player2))
    g.new_game()
    layout = 'base'

    try:
        g.load_layout(f'layouts/{layout}.csv')
    except:
        g.load_layout(f'Game/layouts/{layout}.csv')

    list_moveable_pieces = []
    playing = True
    while playing:
        list_moveable_pieces = []
        clear_screen()
        g.print()

        print(f'Player: {g.current_player.name}')
        print()

        for piece in g.pieces:
            if piece.color == g.current_player.color and g.get_piece_move_tree(piece).size() > 1:
                list_moveable_pieces.append(
                    g.position_to_anotation(piece.position))

        if list_moveable_pieces == []:
            print(f"{g.next_player.name} VYHRÁL")
            break
        print(
            f"You can move pieces on these positions: {list_moveable_pieces}")
        annotation_input = input("which piece do you want to move ? ")
        try:
            piece = g.board[g.anotation_to_position(annotation_input)]
        except:
            print("It's not a annotation!!")
            input()
            continue

        if annotation_input in list_moveable_pieces:
            moves = g.get_piece_moves(piece)
            move_tree = g.get_piece_move_tree(piece)
            move_id = 0
            end = True
            while end:
                if move_id < len(moves):
                    steps = [move_tree.get_node(
                        node).data for node in moves[move_id]]
                    print(f"\nmove: {move_id+1}\n")
                    input(g.visualize_move(steps))
                    move_id += 1
                else:
                    try:
                        print("write number which move do you want to make.")
                        number_board = int(
                            input("if you dont write any number it will show you again ")) - 1
                        if number_board >= 0 and number_board <= len(moves):
                            end = False
                    except:
                        move_id = 0

            g.make_move(piece, number_board, True)

        else:
            input(f"{annotation_input} is wrong")
            continue
        input()
        g.swap_active_players()


if __name__ == '__main__':
    main()
