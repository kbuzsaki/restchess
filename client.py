from urllib.request import urlopen
import json
import chess
from chess import Board, Color, Position, Piece

LOCALHOST = "http://127.0.0.1:5000"

class GameConnection:

    def __init__(self, base_url):
        self.base_url = base_url

    def _get(self, path, **kwargs):
        url = self.base_url + path

        # assemble url args
        if kwargs:
            url += "?" + "&".join([key + "=" + str(kwargs[key]) for key in kwargs])

        resp = json.loads(urlopen(url).read().decode('utf8'))
        return resp

    def board(self):
        return Board.from_notation(self._get("/board")["board"])

    def turn(self):
        return self._get("/turn")

    def print_board(self):
        pretty(self._get("/board"))

    def move(self, begin, end):
        self._get("/move", begin=begin, end=end)

def pretty(resp):
    board = resp["board"]
    print("it is " + resp["current_player"] + "'s turn!")
    print("     " + "     ".join("ABCDEFGH"))
    for row_num, row in enumerate(board):
        new_row = [el if el else "  " for el in row]
        print(str(row_num + 1) + " " + str(new_row))
    print("     " + "     ".join("ABCDEFGH"))


