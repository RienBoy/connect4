"""
Main entry in a connect 4 game.
Handles the printing, input and player turns.
"""
import random
import re

from blessed import Terminal
from . import c4

t = Terminal()

with t.location():
    print('Starting game...')


pcolor = {
    1: t.blue,
    2: t.red
}

status_message, status_message_nf = None, None
cur_player = None


def set_status_message(msg):
    """Sets the global `status_message` and unformat `status_message_nf`"""
    global status_message
    global status_message_nf
    ansi_escape = re.compile(r'''
        \x9B|\x1B    # ESC
        (?:     # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
        |       # or [ for CSI, followed by a control sequence
            [\[(]
            [0-?]*  # Parameter bytes
            [ -/]*  # Intermediate bytes
            [@-~]   # Final byte
        )
    ''', re.VERBOSE)
    status_message = msg
    status_message_nf = ansi_escape.sub('', msg)


def get_input(player):
    """Gets the input from player `player`and puts a disc."""
    col = None
    print(f'{pcolor[player](f"P{player}")}>>', end="")

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
    """Prints a game state."""
    print(t.clear_eos)
    print(status_message)
    print("=" * len(status_message_nf))
    c4.print_board()


def run_game():
    """Runs the game"""
    cur_player = random.randint(1, 2)  # Choose starting player
    set_status_message(f'{pcolor[cur_player](f"Player {cur_player}")} begins.')

    # First turn
    with t.location(): 
        print_game()
        get_input(cur_player)

    # As long as the game isn't won
    while not c4.check_win(cur_player):
        cur_player = 1 - (cur_player-1) + 1
        set_status_message(f'{pcolor[cur_player](f"Player {cur_player}")}\'s turn')
        with t.location():
            print_game()
            get_input(cur_player)

    # Game is won
    set_status_message(f'{t.bold(pcolor[cur_player](f"Player {cur_player}"))} won the game!')
    print_game()
    print()


try:
    run_game()
except KeyboardInterrupt:
    # Game is interrupted
    print_game()
    print('\nGame interupted by KeyboardInterrupt')
