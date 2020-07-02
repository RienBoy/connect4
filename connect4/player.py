"""
Implements a player to play connect4 with.
"""
import socket
import pickle

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


class LocalPlayer(Player):
    def __init__(self, name, selfip=""):
        # Setup the connection
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((selfip, 4445))
        super().__init__(name)


    def connect(self, conn, starting_player=None):
        self.s.connect((conn, 4444))
        self.s.sendall(pickle.dumps([self.name, starting_player]))


    def do_turn(self, board):
        # do turn
        choice = super().do_turn(board)
        # send choice to remote
        self.s.sendall(pickle.dumps(choice))

        # return choice
        return choice


    def close(self):
        self.s.close()


class RemotePlayer(Player):
    def __init__(self, selfip=""):
        # Setup the connection
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((selfip, 4444))
        self.s.listen()
        print(f'Listening on {selfip if selfip else socket.gethostbyname(socket.gethostname())}')
        
        super().__init__('Remote player')


    def accept(self):
        (self.conn, addr) = self.s.accept()
        (self.name, starting_player) = pickle.loads(self.conn.recv(1024))
        return addr[0], starting_player


    def do_turn(self, board):
        # Receive choice from other player
        choice = pickle.loads(self.conn.recv(1024))

        # Apply choice
        c4.put_disc(board, self.number + 1, choice)

        # Return choice
        return choice


    def close(self):
        self.conn.shutdown(socket.SHUT_RDWR)
        self.s.close()
