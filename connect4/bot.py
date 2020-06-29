import random
from copy import deepcopy
from statistics import mean

from . import c4


class Bot:
    def __init__(self, board, difficulty, number):
        self.board = board
        self.difficulty = difficulty
        self.number = number
        self.color = c4.pcolor[number]
    

    def do_turn(self):
        chances = self.calculate_chances(0)
        max_chances = [i for i, v in enumerate(chances) if v == max(chances)]
        choice = random.choice(max_chances) + 1
        c4.put_disc(self.number, choice)
        return choice
    

    def calculate_chances(self, level):
        chances = []
        for col in range(c4.COLUMNS):
            if level == self.difficulty:
                chances.append(self.longest_streak(col+1))
            else:
                chances.append(mean(self.calculate_chances(level+1)))
        return chances


    def longest_streak(self, col):
        max_streak = 0
        for player in (2, 1): # win first, lose second
            test_board = deepcopy(self.board)
            c4.put_disc(player, col, test_board)
            for row in range(c4.ROWS):
                for column in range(c4.COLUMNS):
                    if test_board[row][column] != player:
                        continue
                    for dx, dy in ((1, -1), (1, 0), (1, 1), (0, 1)):
                        new_streak = self.streak(player, test_board, row, column, dx, dy)
                        max_streak = max_streak if max_streak >= new_streak else new_streak
                        if max_streak >= 4:
                            return max_streak # let's cut it short
        return max_streak
            

    def streak(self, player, board, row, column, dx, dy):
        for scale in range(4):
            if (not (0 <= row + dy*scale < c4.ROWS) or not (0 <= column + dx*scale < c4.COLUMNS)):
                return scale
            if board[row + dy * scale][column + dx * scale] != player:
                return scale
        return 4


    def __str__(self):
        return self.color('Bot')


    def __repr__(self):
        return self.color(f'Bot({self.number})')
