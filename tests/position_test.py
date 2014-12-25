import unittest
import chess
import itertools
from chess import Position

class PositionTest(unittest.TestCase):

    def setUp(self):               
        self.positions = [[Position(row, col) for col in range(8)] for row in range(8)]
        self.flat_positions = set(itertools.chain(*self.positions))
        self.notations = [["A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1"],
                          ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2"],
                          ["A3", "B3", "C3", "D3", "E3", "F3", "G3", "H3"],
                          ["A4", "B4", "C4", "D4", "E4", "F4", "G4", "H4"],
                          ["A5", "B5", "C5", "D5", "E5", "F5", "G5", "H5"],
                          ["A6", "B6", "C6", "D6", "E6", "F6", "G6", "H6"],
                          ["A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7"],
                          ["A8", "B8", "C8", "D8", "E8", "F8", "G8", "H8"]]

    def test_from_notation(self):
        for notation_row, position_row in zip(self.notations, self.positions):
            for notation, position in zip(notation_row, position_row):
                self.assertEqual(position, Position.from_notation(notation))

    def test_str(self):
        for notation_row, position_row in zip(self.notations, self.positions):
            for notation, position in zip(notation_row, position_row):
                self.assertEqual(notation, str(position))

    def test_repr(self):
        for position in self.flat_positions:
            # repr should be a constructor call, so eval should produce an equivalent point
            self.assertEqual(position, eval(repr(position)))

    def test_eq_hash(self):
        for row, position_row in enumerate(self.positions):
            for col, position in enumerate(position_row):
                others = self.flat_positions - {position}
                # test equality
                self.assertEqual(position, Position(row, col))
                self.assertFalse(any(position == other for other in others))
                # test hash
                self.assertIn(position, self.flat_positions)
                self.assertNotIn(position, others)

    def test_iter(self):
        for position in self.flat_positions:
            row, col = position
            self.assertEqual(position.row, row)
            self.assertEqual(position.col, col)

    def test_add(self):
        pass

    def test_pass(self):
        pass

if __name__ == '__main__':
    unittest.main()
