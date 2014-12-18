from enum import Enum, unique

@unique
class Color(Enum):
    white = 1
    black = 2

    def __str__(self):
        return self.name


ROWS = ["1", "2", "3", "4", "5", "6", "7", "8"]
COLS = ["A", "B", "C", "D", "E", "F", "G", "H"]

class Position:

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return COLS[self.col] + ROWS[self.row]

    def __repr__(self):
        return "chess.Position(row=" + str(self.row) + ", col=" + str(self.col) + ")"

    def __iter__(self):
        yield self.row
        yield self.col

    def __add__(self, delta):
        drow, dcol = delta
        return Position(self.row + drow, self.col + dcol)

    def __sub__(self, other):
        row, col = other
        return (self.row - row, self.col - col)

