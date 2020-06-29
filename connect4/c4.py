from blessed import Terminal
from IPython import embed


COLUMNS = 7
ROWS = 6

t = Terminal()

board = [[0 for column in range(COLUMNS)] for row in range(ROWS)]
signs = {
    0: t.white('O'),
    1: t.blue('O'),
    2: t.red('O')
}


def put_disc(player, column):
    row = -1
    column -= 1
    while board[row][column]:
        row -= 1
        if row < -ROWS:
            return False
    board[row][column] = player
    return True


def check_win(player):
    def check_pos(row, column):
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
    print(t.bold_underline_yellow("1 2 3 4 5 6 7"))
    for row in board:
        for cell in row:
            print(signs[cell], end=" ")
        print()


if __name__ == '__main__':
    embed()
