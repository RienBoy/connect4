import random

from blessed import Terminal
from . import c4

t = Terminal()

with t.location():
    print('Starting game...')


pcolor = {
    1: t.blue,
    2: t.red
}


def get_input(player):
    col = None
    print(f'{pcolor[cur_player](f"P{cur_player}")}>>', end="")

    with t.cbreak():
        while True:
            key = t.inkey()
            if key == '\x03': # Ctrl+C
                raise KeyboardInterrupt

            if key.is_sequence and key.code == t.KEY_ENTER and col is not None:
                if c4.put_disc(player, col):
                    break

            if not key.is_sequence and key in (str(x+1) for x in range(c4.COLUMNS)):
                col = int(key)

            if col is not None:
                print(col, end="\b")


def print_game():
    print(t.clear_eos)
    print(status_message)
    print("=" * len(status_message))
    c4.print_board()


try:
    cur_player = random.randint(1, 2)
    status_message = f'{pcolor[cur_player](f"Player {cur_player}")} begins.'

    with t.location():
        print_game()
        get_input(cur_player)

    while not c4.check_win(cur_player):
        cur_player = 1 - (cur_player-1) + 1
        with t.location():
            status_message = f'{pcolor[cur_player](f"Player {cur_player}")}\'s turn'
            print_game()
            get_input(cur_player)

    status_message = f'{t.bold(pcolor[cur_player](f"Player {cur_player}"))} won the game!'
    print_game()
    print()

except KeyboardInterrupt:
    print_game()
    print('\nGame interupted by KeyboardInterrupt')
