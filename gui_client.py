from tkinter import *
from enum import Enum, unique
import chess
from chess import Position

class Window(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")   
        self.parent = parent
        self.parent.title("Chess!")

        # initialize buttons container
        self.grid(sticky=N+S+E+W)
        for index in range(8):
            self.rowconfigure(index, weight=1)
            self.columnconfigure(index, weight=1)

        # grid of buttons corresponding to board squares
        self.buttons = [[None] * 8 for x in range(8)]
        self.selected = None

        self.board = chess.Board.from_notation(chess.STARTING_NOTATION)
        self.reload_board()

    def reload_board(self):
        for row_num, row in enumerate(self.board.rows):
            for col_num, square in enumerate(row):
                button = SquareButton(self, self.buttons, self.board, row_num, col_num)
                self.buttons[row_num][col_num] = button

    def reset_all(self):
        self.selected = None
        for button_row in self.buttons:
            for button in button_row:
                button.reset()

    def on_click(self, button):
        if button is self.selected or not self.selected and not button.empty:
            button.toggle_selected()
            self.selected = button if button.selected else None
            # reset if unclick
            if not button.selected:
                self.reset_all()
            else:
                for position in button.piece.possible_moves:
                    self.buttons[position.row][position.col].set_movable()
                for position in button.piece.possible_attacks:
                    self.buttons[position.row][position.col].set_attackable()
        if button.movable or button.attackable:
            self.selected.piece.move_to(button.position)
            self.reset_all()


@unique
class State(Enum):
    blank = 1
    selected = 2
    movable = 3
    attackable = 4

class SquareButton(Label):

    def __init__(self, window, buttons, board, row, col):
        Label.__init__(self, window)
        self.window = window
        self.buttons = buttons
        self.board = board
        self.row = row
        self.col = col
        self.state = State.blank

        self["highlightbackground"] = "black"
        self["highlightthickness"] = 1
        self.bind("<Button-1>", self.on_click)
        self.grid(sticky=N+S+E+W, row=row, column=col)
        self.blob = None
        self.reset()

    def update_text(self):
        square = self.board[self.row][self.col]
        self["text"] = square.to_notation() if square else "  "

    def reset(self):
        self.state = State.blank
        self["fg"] = "black"
        self["font"] = "-weight normal"
        self["bg"] = "cornsilk3" if self.is_dark else "linen"
        self.update_text()
        if self.blob:
            self.blob.destroy()

    @property
    def is_dark(self):
        return (self.row + self.col) % 2 == 0

    @property
    def selected(self):
        return self.state == State.selected

    @property
    def movable(self):
        return self.state == State.movable

    @property
    def attackable(self):
        return self.state == State.attackable

    @property
    def position(self):
        return Position(self.row, self.col)

    @property
    def piece(self):
        return self.board.at(self.position)

    @property
    def empty(self):
        return self.board.empty(self.position)

    def set_blob(self, color):
        self["text"] = "@"
        self["font"] = "-weight bold"
        self["fg"] = color

    def set_selected(self):
        self.state = State.selected
        self["bg"] = "goldenrod" if self.is_dark else "pale goldenrod"

    def set_movable(self):
        self.state = State.movable
        self.set_blob("dark turquoise" if self.is_dark else "turquoise")

    def set_attackable(self):
        self.state = State.attackable
        self["bg"] = "pink"

    def toggle_selected(self):
        if self.selected:
            self.reset()
        else:
            self.set_selected()

    def on_click(self, event):
        self.window.on_click(self)

        
if __name__ == '__main__':
    root = Tk()
    root.geometry("420x360+800+300")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    app = Window(root)

    root.mainloop()  
