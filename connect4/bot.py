"""
Implements a Bot to play connect4.
"""
import random
from copy import deepcopy
from statistics import mean

from . import c4


class Quatro:
    """Represents a Bot that can play connect4"""
    def __init__(self, difficulty):
        """Initializes the Bot

        Arguments:
         - board: handle to the game board
         - dificulty: difficulty of the Bot
         - number: identifying number of the bot
        """
        self.difficulty = difficulty
        self.number = None
        self.color = None
        self.opponent = None
        self.name = 'Quatro'


    def give_number(self, number):
        """Sets the identification number of the bot."""
        self.number = number
        self.color = c4.pcolor[number + 1]
        self.opponent = 1 - self.number


    def do_turn(self, board):
        """Executes a turn for this Bot"""
        chances = self.calculate_chances(board)
        max_chances = [i for i, v in enumerate(chances) if v == max(chances)]
        choice = random.choice(max_chances) + 1
        c4.put_disc(board, self.number + 1, choice)
        return choice
    

    def calculate_chances(self, board):
        """
        Calculate the chances of each column to win the game if Bot puts a disc there.

        Arguments:
         - board: the board on which to calculate the chances
        """
        chances_win = []
        for col in range(c4.COLUMNS):
            test_board = deepcopy(board)
            if c4.put_disc(test_board, self.number + 1, col + 1):
                chances_win.append(c4.max_streak(test_board, self.number + 1))
            else:   # column full
                chances_win.append(0)
        if any(x >= 4 for x in chances_win):
            return chances_win  # Immediate victory

        chances_lose = []
        for col in range(c4.COLUMNS):
            test_board = deepcopy(board)
            if c4.put_disc(test_board, self.opponent + 1, col + 1):
                chances_lose.append(c4.max_streak(test_board, self.opponent + 1))
            else:   # column full
                chances_lose.append(0)
        if any(x >= 4 for x in chances_lose):
            return chances_lose # Immediate loss
        
        chances_lose_on_second = []
        for col in range(c4.COLUMNS):
            test_board = deepcopy(board)
            c4.put_disc(test_board, self.number + 1, col + 1)
            chances_lose_on_second.append([])
            for col_2 in range(c4.COLUMNS):
                test_board_2 = deepcopy(test_board)
                if c4.put_disc(test_board_2, self.opponent + 1, col_2 + 1):
                    chances_lose_on_second[col].append(c4.max_streak(test_board_2, self.opponent + 1))
                else:   # column full
                    chances_lose_on_second[col].append(0)
        # Don't place when oppenent can win next round (0.1 in case all else is full)
        return [any(0.1 if x >= 4 else 1 for x in l2) * w for l2, w in zip(chances_lose_on_second, chances_win)]


    def __str__(self):
        return self.color(self.name)


    def __repr__(self):
        return self.color(self.name + f'({self.number})')
