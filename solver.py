from tkinter import *
from tkinter import ttk
import numpy as np
from web import web_download
from grid import Grid


class Gui:
    def __init__(self, _title, _w, _h):
        # initialize GUI
        self.master = Tk()
        self.master.title(_title)
        self.master.title(_title)
        self.master.geometry(str(_w) + 'x' + str(_h))
        # initialize squares
        self.squares = []
        self.notebook = ttk.Notebook(self.master)
        # potentially more tabs and compare by changing puzzle_num
        puzzle_num = 1
        for i in range(0, puzzle_num):
            page = self.__add_tab('Puzzle ' + str(i + 1), _w, _h)
            self.squares.append(self.lay_grid(page))
        self.notebook.select(0)

    # draws the grid and buttons
    def lay_grid(self, page):
        squares = np.empty((9, 9), dtype=ttk.Entry)
        frame_grid = Frame(page, relief=GROOVE, borderwidth="2", background="cornflower blue")
        frame_grid.place(relx=0.02, rely=0.08, relheight=0.75, relwidth=0.75)
        edge = 0.001
        space = 1 / 9.0 - 4 / 3 * edge
        y = 3 * edge
        for r in range(0, 9):
            x = edge * 3
            for c in range(0, 9):
                box = ttk.Entry(frame_grid, font=('Courier', '18', 'bold'), justify='center')
                box.place(relx=x, rely=y, relheight=space, relwidth=space)
                box.bind("<Leave>", validate_int)
                squares[r, c] = box
                x += space + (3 * edge if c in [2, 5] else 0)
            y += space + (3 * edge if r in [2, 5] else 0)

        # make the buttons
        btn = Button(page, text='Web Sudoku', bg='light blue', fg='green', font=('New Roman', '14', 'bold'),
                     command=self.upload_it)
        btn.place(relx=0.02, rely=0.85, relheight=0.08, relwidth=0.2)
        btn = Button(page, text='Solve', bg='light blue', fg='blue', font=('New Roman', '14', 'bold'),
                     command=self.solve_it)
        btn.place(relx=0.25, rely=0.85, relheight=0.08, relwidth=0.2)
        btn = Button(page, text='Clear', bg='light blue', fg='red', font=('New Roman', '14', 'bold'),
                     command=self.clear_it)
        btn.place(relx=0.47, rely=0.85, relheight=0.08, relwidth=0.2)
        return squares

    # called by initializer puzzle_num number of times to make tabs, makes one tab each time
    def __add_tab(self, _text, _w, _h):
        tab = ttk.Frame(self.notebook, width=_w, height=_h)
        self.notebook.grid()
        self.notebook.add(tab, text=_text)
        return tab

    # calls the solver in Grid and prints out the solution
    # If there is no solution, add to all non-numerical cells a red 'X'
    def solve_it(self):
        stop = False
        ndx = self.notebook.index(self.notebook.select())
        # retrieving values from the gui and sends it to the solver
        given = np.empty((9, 9), dtype=int)
        for r in range(0, len(self.squares[ndx])):
            if stop:
                break
            for c in range(0, len(self.squares[ndx])):
                x = self.squares[ndx][r, c].get()
                if x != '' and not x.isnumeric():
                    stop = True
                    break
                elif x == '':
                    given[r, c] = 0
                else:
                    if 0 < int(x) < 10:
                        given[r, c] = int(x)
                    else:
                        stop = True
                        break
        if stop:
            solution = None
        else:
            solution = Grid.solve(given)
        # if there is a solution, print the solution with the new numbers in red
        if solution is not None:
            for r in range(0, len(self.squares[ndx])):
                for c in range(0, len(self.squares[ndx])):
                    fg = 'black' if given[r, c] != 0 else 'red'
                    self.squares[ndx][r, c].config(foreground=fg)
                    self.squares[ndx][r, c].delete(0, 'end')
                    self.squares[ndx][r, c].insert(0, solution[r, c])
        # if there is no solution, the red X as explained above
        else:
            for r in range(0, len(self.squares[ndx])):
                for c in range(0, len(self.squares[ndx])):
                    if given[r, c] == 0:
                        self.squares[ndx][r, c].config(foreground='red')
                        self.squares[ndx][r, c].insert(0, 'X')
        return

    # Get the puzzle from the web
    def upload_it(self):
        self.clear_it()
        ndx = self.notebook.index(self.notebook.select())
        given = web_download()
        for r in range(0, 9):
            for c in range(0, 9):
                if given[r, c] != 0:
                    self.squares[ndx][r, c].insert(0, str(given[r, c]))

    # Clear the grid
    def clear_it(self):
        ndx = self.notebook.index(self.notebook.select())
        for r in range(0, 9):
            for c in range(0, 9):
                self.squares[ndx][r, c].delete(0, 'end')
                self.squares[ndx][r, c].config(foreground='black')


# Makes sure the number is valid, otherwise, empty the number
def validate_int(event):
    if event.widget.get() == '':
        return
    try:
        n = int(event.widget.get())
        if n < 1 or n > 9:
            raise Exception('')
    except:
        event.widget.delete(0, 'end')
        event.widget.insert(0, '')


# run the program
if __name__ == '__main__':
    gui = Gui('Option Model', 700, 700)
    gui.master.mainloop()