from urllib.request import urlopen
import json

BASE_URL = "http://127.0.0.1:5000"

def get(args):
    url = BASE_URL + args
    resp = json.loads(urlopen(url).read().decode('utf8'))
    if "error" in resp:
        print("ERROR: " + resp["error"])
    return resp

def board():
    pretty(get("/board"))

def move(begin, end):
    pretty(get("/move?begin=" + str(begin) + "&end=" + str(end)))

def pretty(resp):
    board = resp["board"]
    print("it is " + resp["current_player"] + "'s turn!")
    print("     " + "     ".join("ABCDEFGH"))
    for row_num, row in enumerate(board):
        new_row = [el if el else "  " for el in row]
        print(str(row_num + 1) + " " + str(new_row))
    print("     " + "     ".join("ABCDEFGH"))


