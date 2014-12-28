from flask import Flask, request
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
game.board = Board.from_notation(STARTING_NOTATION)

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

@app.route('/board')
def display_board(extras=dict()):
    display = {"turn": game.turn, "current_player": str(game.cur_player), "board": game.board.to_notation()}
    display.update(extras)
    return json.dumps(display)
    
@app.route('/move')
def next_move():
    begin_position = Position.from_notation(request.args.get("begin", ""))
    end_position = Position.from_notation(request.args.get("end", ""))
    begin_piece = game.board.at(begin_position)
    end_piece = game.board.at(end_position)

    if game.board.empty(begin_position):
        return display_board(extras={"error": "no piece at position: " + str(begin_position)})
    if begin_piece.color != game.cur_player:
        return display_board(extras={"error": "that piece is not " + str(game.cur_player)})

    if game.board.empty(end_position) and not begin_piece.valid_move(end_position):
        return display_board(extras={"error": "you cannot move there!"})
    if not game.board.empty(end_position) and not begin_piece.valid_attack(end_position):
        return display_board(extras={"error": "you cannot attack that piece!"})

    begin_piece.move_to(end_position)
    game.next_turn()

    return display_board()

if __name__ == "__main__":
    app.run(debug=True)
