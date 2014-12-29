from urllib.request import urlopen
import json
import chess
from chess import Board, Color, Position, Piece

LOCALHOST = "http://127.0.0.1:5000"

class GameConnection:

    def __init__(self, base_url):
        self.base_url = base_url
        self.invalidated = True
        print("initializing connection to: " + base_url)
        self._validate() # does the first load
        print("initialized connection to: " + base_url)

    def _get(self, path, **kwargs):
        url = self.base_url + path

        # assemble url args
        if kwargs:
            url += "?" + "&".join([key + "=" + str(kwargs[key]) for key in kwargs])

        resp = json.loads(urlopen(url).read().decode('utf8'))
        return resp

    def _validate(self):
        if self.invalidated:
            self._cached_board = Board.from_notation(self._get("/board")["board"])
            self.invalidated = False

    def refresh(self):
        self.invalidated = True

    def board(self):
        self._validate()
        return self._cached_board

    def turn(self):
        return self._get("/turn")

    def print_board(self):
        pretty(self._get("/board"))

    def move(self, begin, end):
        self._get("/move", begin=begin, end=end)
        self.refresh()

def pretty(resp):
    board = resp["board"]
    print("it is " + resp["current_player"] + "'s turn!")
    print("     " + "     ".join("ABCDEFGH"))
    for row_num, row in enumerate(board):
        new_row = [el if el else "  " for el in row]
        print(str(row_num + 1) + " " + str(new_row))
    print("     " + "     ".join("ABCDEFGH"))


class MockGameConnection:

    def __init__(self):
        self._board = Board.from_notation(chess.STARTING_NOTATION)
        self.turn_count = 1
        self.cur_player = Color.white
        print("initialized mock connection")

    def _next_turn(self):
        if self.cur_player == Color.white:
            self.cur_player = Color.black
        else:
            self.turn_count += 1
            self.cur_player = Color.white

    def refresh(self):
        # no op because it's all local
        pass

    def board(self):
        return self._board

    def turn(self):
        return {"turn": self.turn_count, "current_player": self.cur_player}

    def print_board(self):
        pretty({"board": self._board.to_notation(), "current_player": str(self.cur_player)})

    def move(self, begin, end):
        begin_position = Position.from_notation(str(begin))
        end_position = Position.from_notation(str(end))
        self._board.at(begin_position).move_to(end_position)

