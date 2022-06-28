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

    while True:
        clear_screen()
        g.print()
        
        print(f'Player: {g.current_player.name}')
        
        input()

        g.swap_active_players()

if __name__ == '__main__':
    main()