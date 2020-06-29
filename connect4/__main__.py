"""
Main entry in a connect 4 game.
Handles the printing, input and player turns.
"""
import random
import re

from blessed import Terminal
from . import c4    # If PyLint shows an error here, don't fix it, it works. PyLint is wrong.
from .bot import Bot
from .player import Player

t = Terminal()

with t.location():
    print('Starting game...')

choice_message = ''
status_message, status_message_nf = None, None
players = []
cur_player = None


def set_choice_message(player, choice):
    """Sets the global `choice_message`"""
    global choice_message
    choice_message = f'{player} chose {choice}.'


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


def print_game():
    """Prints a game state."""
    print(t.clear_eos)
    print(choice_message)
    print(status_message)
    print("=" * len(status_message_nf))
    c4.print_board()


def run_game():
    """Runs the game"""
    global cur_player
    set_status_message(f'{players[cur_player]} begins.')

    # First turn
    with t.location(): 
        print_game()
        choice = players[cur_player].do_turn()
        set_choice_message(players[cur_player], choice)

    # As long as the game isn't won
    while not c4.check_win(cur_player + 1):
        cur_player = 1 - cur_player
        set_status_message(f'{players[cur_player]}\'s turn')
        with t.location():
            print_game()
            choice = players[cur_player].do_turn()
            set_choice_message(players[cur_player], choice)

    # Game is won
    set_status_message(f'{t.bold(str(players[cur_player]))} won the game!')
    print_game()
    print()


try:
    players.append(Player('Player 1', 1))
    players.append(Bot(c4.board, 0, 2))
    #players.append(Player('Player 2', 2))
    cur_player = random.randint(0, 1)
    run_game()
except KeyboardInterrupt:
    # Game is interrupted
    print_game()
    print('\nGame interupted by KeyboardInterrupt')
