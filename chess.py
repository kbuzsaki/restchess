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

    @classmethod
    def from_notation(constructor, notation):
        col_name, row_name = notation
        row = ROWS.index(row_name)
        col = COLS.index(col_name)
        return constructor(row, col)

    def __str__(self):
        return COLS[self.col] + ROWS[self.row]

    def __repr__(self):
        return "chess.Position(row=" + str(self.row) + ", col=" + str(self.col) + ")"

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash(self.row) ^ hash(self.col)

    def __iter__(self):
        yield self.row
        yield self.col

    def __add__(self, delta):
        drow, dcol = delta
        return Position(self.row + drow, self.col + dcol)

    def __sub__(self, other):
        row, col = other
        return (self.row - row, self.col - col)


class Piece:

    def __init__(self, color, position, board):
        self.color = color
        self.position = position
        self.board = board

    @property
    def row(self):
        return self.position.row

    @property
    def col(self):
        return self.position.col


class Pawn(Piece):

    def _can_en_passant(self):
        return (self.color, self.row) in [(Color.white, 1), (Color.black, 7)]

    def valid_move(self, new_position):
        drow, dcol = new_position - self.position

        # en passant movement
        if (drow, dcol) == (0, 2) and self._can_en_passant():
            return board.empty(self.position + (0, 1)) and board.empty(self.position + (0, 2))
        # normal movement
        elif (drow, dcol) == (0, 1):
            return not board[self.row][self.col + 1]

    def valid_attack(self, position):
        drow, dcol = position - self.position

        # if the movement is right
        if (drow, dcol) in [(1, 1), (-1, 1)]:
            return not board.empty(position) and self.color != board.at(position).color

