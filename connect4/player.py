"""
Implements a player to play connect4 with.
"""
from blessed import Terminal
from . import c4

from time import sleep


class Player:
    """Represents a Player"""
    def __init__(self, name):
        """Initializes the Player.

        Arguments:
         - name: the name of the player
         - number: identifying number of the player
        """
        self.color = None
        self.name = name
        self.number = None
        self.t = Terminal()


    def give_number(self, number):
        """Sets the identification number of the player."""
        self.number = number
        self.color = c4.pcolor[number + 1]


    def do_turn(self, board):
        """Gets the input from player `player`and puts a disc."""
        col = None
        print(f'{self}>>', end="", flush=True)

        with self.t.cbreak():
            while True:
                key = self.t.inkey()
                if key == '\x03': # Ctrl+C
                    raise KeyboardInterrupt

                if key.is_sequence and key.code == self.t.KEY_ENTER and col is not None:
                    if c4.put_disc(board, self.number + 1, col):
                        return col

                if not key.is_sequence and key in (str(x+1) for x in range(c4.COLUMNS)):
                    col = int(key)

                if col is not None:
                    print(col, end="\b", flush=True)


    def __str__(self):
        return self.color(self.name)


    def __repr__(self):
        return self.color(f'{self.name}({self.number})')
