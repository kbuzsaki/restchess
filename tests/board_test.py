import unittest
import chess
import itertools
from chess import Board

class BoardTest(unittest.TestCase):

    def test_empty(self):
        board = Board()
        self.assertTrue(all(board.empty((row, col)) for row in range(8) for col in range(8)))

if __name__ == '__main__':
    unittest.main()
