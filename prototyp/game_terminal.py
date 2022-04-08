from core import *

def main():
    p1n = input('Player 1 name:\n')
    p2n = input('Player 2 name:\n')
    
    player1 = Player(p1n, True)
    player2 = Player(p2n)
    
    g = Board((player1, player2))
    current_player = player1
    other_player = player2
    while True:
        print('\x1B[0;0H\x1B[J')
        g.print(numbers=True)
        print(f'Player: {current_player._name}')
        vp = current_player.get_valid_plays()
        if not vp:
            print(f'Player {other_player._name} wins!')
            break
        print(vp)
        while True:
            p = input('Piece: ')
            if p == 'x' or int(p) in vp.keys(): break
            print('invalid selection')
        if p == 'x': break
        p = int(p)
        while True:
            m = input('Move index: ')
            try:
                if int(m) in range(len(vp[p])): break
            except:
                pass
            print('invalid selection')
        current_player.play(p, int(m))
        current_player, other_player = other_player, current_player 


if __name__ == '__main__':
    main()