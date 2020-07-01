"""
c4 implements function for the main mechanics of the game:
 - keeps track of the board
 - put discs in the board
 - check for wins
 - displays the board
"""
import random

from blessed import Terminal
from IPython import embed

# CONSTANTS
COLUMNS = 7
ROWS = 6

# Terminal
t = Terminal()

# Player colors
# 0 is empty
pcolor = {
    0: lambda x: t.white(x),
    1: lambda x: t.blue(x),
    2: lambda x: t.red(x)
}

def put_disc(board, player, column):
    """
    Puts a disc of player `player` in column `column`.
    Returns `False` if the column is full.
    """
    row = -1
    column -= 1
    while board[row][column]:
        row -= 1
        if row < -ROWS:
            return False
    board[row][column] = player
    return True


def max_streak(board, player):
    """Finds the longest streak `player` has on `board`."""
    max_s = 0
    for row in range(ROWS):
        for column in range(COLUMNS):
            if board[row][column] != player: 
                continue
            for dx, dy in ((1, -1), (1, 0), (1, 1), (0, 1)):
                s = streak(board, player, row, column, dx, dy)
                max_s = max_s if max_s >= s else s
    return max_s


def streak(board, player, row, column, dx, dy):
    """Calculates the streak of `player` on `board` starting from [`row`, `column`] in direction (`dx`, `dy`)."""
    scale = 0
    while True:
        if not (0 <= row + dy * scale < ROWS and 0 <= column + dx * scale < COLUMNS):
            return scale
        if board[row + dy * scale][column + dx * scale] != player:
            return scale
        scale += 1


class Connect4Game:
    """Implements the functionalities and keeps track of a game of connect 4."""
    def __init__(self, player1, player2):
        """
        Initializes a game.
        
        Arguments:
         - player1: The first player
         - player2: The second player
        """
        self.board = [[0 for column in range(COLUMNS)] for row in range(ROWS)]
        self.signs = {key: color('O') for key, color in pcolor.items()}
        player1.give_number(0)
        player2.give_number(1)
        self.players = (player1, player2)
        self.cur_player = random.randint(0, 1)


    def __str__(self):
        """Prints the board"""
        output = ''
        output += t.bold_underline_yellow("1 2 3 4 5 6 7") + '\n'
        for row in self.board:
            for cell in row:
                output += self.signs[cell] + " "
            output += '\n'
        return output


    def turn(self):
        """
        Executes a turn in game and set current_player to the next player.
        
        Returns the player that went and the choice of that player.
        """
        choice, player = self.get_current_player().do_turn(self.board), self.get_current_player()
        self.cur_player = 1 - self.cur_player
        return player, choice


    def check_win(self):
        """Checks if the game has been won by the player that just went."""
        max_s = max_streak(self.board, self.get_previous_player().number + 1)
        return max_s >= 4


    def put_disc(self, player, column):
        """Puts a disc of `player` in `column`"""
        return put_disc(self.board, player.number + 1, column)


    def get_current_player(self):
        """Returns the currents turn's player."""
        return self.players[self.cur_player]


    def get_previous_player(self):
        """Returns the previous turn's player."""
        return self.players[1 - self.cur_player]
