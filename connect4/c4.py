"""
c4 implements function for the main mechanics of the game:
 - keeps track of the board
 - put discs in the board
 - check for wins
 - displays the board
"""
from blessed import Terminal
from IPython import embed

# CONSTANTS
COLUMNS = 7
ROWS = 6

# Terminal
t = Terminal()

# Board
board = [[0 for column in range(COLUMNS)] for row in range(ROWS)]
# Display characters
signs = {
    0: t.white('O'),
    1: t.blue('O'),
    2: t.red('O')
}


def put_disc(player, column):
    """
    Puts a disc of player `player`in column `column`.
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


def check_win(player):
    """Checks if player `player` has won the game."""
    def check_pos(row, column):
        """Check if a streak of 4 starts from given position."""
        for dx, dy in ((1, -1), (1, 0), (1, 1), (0, 1)):
            count = 0
            for scale in range(4):
                if (row + dx*scale >= ROWS or column + dy*scale >= COLUMNS): continue
                if board[row + dx * scale][column + dy * scale] == player:
                    count += 1
                    if count == 4:
                        return True
        return False

    for row in range(ROWS):
        for column in range(COLUMNS):
            if board[row][column] != player: continue
            if check_pos(row, column):
                return True
    return False


def print_board():
    """Prints the board"""
    print(t.bold_underline_yellow("1 2 3 4 5 6 7"))
    for row in board:
        for cell in row:
            print(signs[cell], end=" ")
        print()


if __name__ == '__main__':
    embed()
