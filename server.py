from flask import Flask
import json
from chess import *

class Game:

    def __init__(self):
        self.turn = 1
        self.cur_player = Color.white

    def next_turn(self):
        if self.cur_player == Color.white:
            self.cur_player = Color.black
        else:
            self.turn += 1
            self.cur_player = Color.white


game = Game()
game.board = Board.from_notation([["WR",   "",   "",   "",   "",   "",   "", "WR"],
                                  ["WP", "WP", "WP", "WP",   "", "WP", "WP", "WP"], 
                                  [  "",   "",   "",   "",   "",   "",   "",   ""],
                                  [  "",   "",   "",   "", "WP",   "",   "",   ""],
                                  [  "",   "",   "",   "", "BP",   "",   "",   ""],
                                  [  "",   "",   "",   "",   "",   "",   "",   ""],
                                  ["BP", "BP", "BP", "BP",   "", "BP", "BP", "BP"], 
                                  ["BR",   "",   "",   "",   "",   "",   "", "BR"]])

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

@app.route('/board')
def display_board():
    display = {"turn": game.turn, "current_player": str(game.cur_player), "board": game.board.to_notation()}
    return json.dumps(display)
    
@app.route('/move')
def next_move():
    game.next_turn()
    return json.dumps({"turn": game.turn, "current_player": str(game.cur_player)})

if __name__ == "__main__":
    app.run(debug=True)
