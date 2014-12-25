from enum import Enum, unique

@unique
class Color(Enum):
    white = 1
    black = 2

    def __str__(self):
        return self.name

    @classmethod
    def from_notation(constructor, notation):
        if notation.lower() == "w":
            return Color.white
        elif notation.lower() == "b":
            return Color.black
        else:
            raise Exception("Couldn't find color for notation: \"" + notation + "\"")

    def to_notation(self):
        if self is Color.white:
            return "w"
        else:
            return "b"



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


class Board:

    def __init__(self):
        self.rows = [[None] * 8 for x in range(8)]

    @classmethod
    def from_notation(constructor, board_notation):
        board = constructor()
        for row, board_row in enumerate(board_notation):
            for col, square in enumerate(board_row):
                if square != "":
                    color_notation, piece_notation = square
                    color = Color.from_notation(color_notation)
                    piece_type = Piece.from_notation(piece_notation)
                    board.add(color, piece_type, Position(row, col))
        return board

    def to_notation(self):
        return [[piece.to_notation() if piece else "" for piece in row] for row in self.rows]

    def __getitem__(self, row):
        return self.rows[row]

    def __contains__(self, position):
        row, col = position
        return 0 <= row < 8 and 0 <= col < 8

    def __iter__(self):
        """iterates over all of the quares in the board """
        for row in self.rows:
            yield from row

    def add(self, color, piece_type, position):
        piece = piece_type(color, position, self)
        self.rows[position.row][position.col] = piece
        return piece

    def at(self, position):
        row, col = position
        return self.rows[row][col]

    def empty(self, position):
        return self.at(position) is None


class Piece:

    def __init__(self, color, position, board):
        self.color = color
        self.position = position
        self.board = board

    @classmethod
    def from_notation(constructor, piece_notation):
        if piece_notation.lower() == "p":
            return Pawn
        else:
            raise Exception("unrecognized piece type: \"" + piece_notation + "\"")

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

    def to_notation(self):
        return self.color.to_notation() + "p"

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



