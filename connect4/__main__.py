"""
Main entry in a connect 4 game.
Handles the printing, input and player turns.
"""
import random
import re

from blessed import Terminal
from . import c4
from .bot import Bot
from .player import Player

t = Terminal()

with t.location():
    print('Starting game...')

game = None
choice_message = ''
status_message, status_message_nf = None, None


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
    print(game)


def run_game():
    """Runs the game"""
    set_status_message(f'{game.get_current_player()} begins.')

    # First turn
    with t.location(): 
        print_game()
        set_choice_message(*game.turn())

    # As long as the game isn't won
    while not game.check_win():
        set_status_message(f'{game.get_current_player()}\'s turn')
        with t.location():
            print_game()
            set_choice_message(*game.turn())

    # Game is won
    set_status_message(f'{t.bold(str(game.get_previous_player()))} won the game!')
    print_game()
    print()


try:
    game = c4.Connect4Game(
        Player('Player 1'),
        Player('Player 2')
    )
    run_game()
except KeyboardInterrupt:
    # Game is interrupted
    print_game()
    print('\nGame interupted by KeyboardInterrupt')
