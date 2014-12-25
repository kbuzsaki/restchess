from flask import Flask
import json
from chess import *

app = Flask(__name__)

turn = 2
cur_player = Color.white
board = Board.from_notation([[  "",   "",   "",   "",   "",   "",   "",   ""],
                             ["WP", "WP", "WP", "WP",   "", "WP", "WP", "WP"], 
                             [  "",   "",   "",   "",   "",   "",   "",   ""],
                             [  "",   "",   "",   "", "WP",   "",   "",   ""],
                             [  "",   "",   "",   "", "BP",   "",   "",   ""],
                             [  "",   "",   "",   "",   "",   "",   "",   ""],
                             ["BP", "BP", "BP", "BP",   "", "BP", "BP", "BP"], 
                             [  "",   "",   "",   "",   "",   "",   "",   ""]])

@app.route('/')
def index():
    return "Hello World!"

@app.route('/board')
def display_board():
    display = {"turn": turn, "current_player": str(cur_player), "board": board.to_notation()}
    return json.dumps(display)
    

if __name__ == "__main__":
    app.run(debug=True)
