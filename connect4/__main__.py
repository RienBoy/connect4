"""
Main entry in a connect 4 game.
Handles the printing, input and player turns.
"""
import argparse
import re

from blessed import Terminal
from . import c4
from .bot import Quatro
from .player import *

parser = argparse.ArgumentParser(description='Play some Connect 4 in the terminal.')
parser.add_argument('player1', nargs='?', default='Player 1', help='Optional name for  player 1')
parser.add_argument('player2', nargs='?', default='Player 2', help='Optional name for  player 2')
group = parser.add_mutually_exclusive_group()
group.add_argument('--bot', '-b', type=int, choices=list(range(1)), default=None, help='Adds a bot with given difficulty')
group.add_argument('--host', action='store_true', help='Host a game of Connect 4')
group.add_argument('--join', help='Join a game of connect 4')
parser.add_argument('--local', '-l', action='store_true', help='Runs the game on local loopback address.\n\t127.0.0.1 for host\n\t127.0.0.2 for join')
args = parser.parse_args()

t = Terminal()

with t.location():
    print('Starting game...')

game = None
player1, player2 = None, None

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
    if args.host:
        player1 = LocalPlayer(args.player1, '127.0.0.1' if args.local else '')
        player2 = RemotePlayer('127.0.0.1' if args.local else '')
        addr, starting_player = player2.accept()
        game = c4.Connect4Game(player1, player2)
        player1.connect(addr, game.get_current_player().number)
    elif args.join is not None:
        player2 = LocalPlayer(args.player1, '127.0.0.2' if args.local else '')
        player2.connect(args.join)
        player1 = RemotePlayer('127.0.0.2' if args.local else '')
        (addr, starting_player) = player1.accept()
        game = c4.Connect4Game(
            player1,
            player2,
            starting_player
        )
    else:
        game = c4.Connect4Game(
            Player(args.player1),
            Quatro(args.bot) if args.bot is not None else Player(args.player2)
        )
    run_game()
except KeyboardInterrupt:
    # Game is interrupted
    if game:
        print_game()
    print('\nGame interupted by KeyboardInterrupt')
except Exception as e:
    print_game()
    print('Connection interrupted. Game stopped.')
finally:
    if player1 and game:
        player1.close()
    if player2 and game:
        player2.close()
