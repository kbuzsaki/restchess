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

    def _enemy_at(self, position):
        return not self.board.empty(position) and self.color != self.board.at(position).color

    def _stop_filter(self, positions):
        for position in positions:
            if position in self.board and self.board.empty(position):
                yield position
            else:
                return

    def _enemy_filter(self, positions):
        return [position for position in positions if self._enemy_at(position)] 

                          
class Pawn(Piece):

    # offsets from this pawn's position for its normal moves, double moves, and attacks
    MOVE_OFFSETS = {Color.white: [(1, 0)], Color.black: [(-1, 0)]}
    DOUBLE_MOVE_OFFSETS = {Color.white: [(1, 0), (2, 0)], Color.black: [(-1, 0), (-2, 0)]}
    ATTACK_OFFSETS = {Color.white: [(1, 1), (1, -1)], Color.black: [(-1, 1), (-1, -1)]}

    def __str__(self):
        return str(self.color).capitalize() + " Pawn, " + str(self.position)

    def __repr__(self):
        return "chess.Pawn(color=" + repr(self.color) + ", position=" + repr(self.position) + ")"

    def _can_double_move(self):
        return (self.color, self.row) in [(Color.white, 1), (Color.black, 6)]

    @property
    def possible_moves(self):
        if self._can_double_move():
            moves = [self.position + offset for offset in Pawn.DOUBLE_MOVE_OFFSETS[self.color]]
        else:
            moves = [self.position + offset for offset in Pawn.MOVE_OFFSETS[self.color]]
        return list(self._stop_filter(moves))

    # TODO: support en passant
    @property
    def possible_attacks(self):
        attacks = [self.position + offset for offset in Pawn.ATTACK_OFFSETS[self.color]]
        return list(self._enemy_filter(attacks))

    def valid_move(self, position):
        return position in self.possible_moves

    def valid_attack(self, position):
        return position in self.possible_attacks



