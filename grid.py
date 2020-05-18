import numpy as np


# the individual squares in the Grid with helper methods
class Cell(object):
    def __init__(self):
        # array of nine booleans, 1 = Possible, 0 = Impossible
        # if a specific index is 0, that means that number is not a valid possibility
        self.values = [1] * 9

    # flips a certain index for value, switches between impossible and possible
    # returns the 1 if value at pos is changed, 0 if otherwise
    def flip(self, pos, v=None):
        if v is None:
            self.values[pos] = 1 - self.values[pos]
            # return 1 serves as a counter, we definitely flipped
            return 1
        # returns 1 if the value actually flipped, otherwise returns 0
        else:
            flipped = 1 if self.values[pos] != v else 0
            self.values[pos] = v
            return flipped

    # flips all values in a cell, returns 9 since that's how many values we flipped
    def flip_all(self, v=None):
        for d in range(0, len(self.values)):
            self.values[d] = 1 - self.values[d] if v is None else v
        return 9

    # get the index of lowest number that's possible
    def get_singular(self):
        for d in range(0, 9):
            if self.values[d] == 1:
                return d
        return None


# A grid is made up of 81 cells
class Grid(object):
    def __init__(self, given=None):
        # initializing those cells
        self.cells = np.empty((9, 9), dtype=Cell)
        for r in range(9):
            for c in range(9):
                self.cells[r, c] = Cell()
        # counts solved cells
        self.singular = 0
        # registry is the count the number of possibilities in each cell
        self.registry = np.ones((9, 9), dtype=int) * 9
        # given is the given numbers of the puzzle
        if given is None:
            return
        (m, m) = given.shape  # should always be 9x9x9 used for potential flexibility in future puzzles
        for r in range(m):
            for c in range(m):
                if given[r, c] >= 1:
                    # we already know the number of that cell, so flip all possibilites in that cell to 0
                    # we don't have to solve it
                    self.cells[r, c].flip_all(0)
                    # we flip back the number given to 1, since this has to be the value
                    self.flip(r, c, given[r, c] - 1, 1)
                    # increment the number of cells that we have solved
                    self.singular += 1
                    # the cell in the registry no only has one possibility, so set that to 1
                    self.registry[r, c] = 1

    # calls flips cell given row and column, d, and v params are passed
    def flip(self, r, c, d, v=None):
        return self.cells[r, c].flip(d, v)

    # checks the cell at current column cc at row r and eliminates possibilities
    def row(self, r, cc):
        # gets smallest value possible in the cell r, cc
        v = self.cells[r, cc].get_singular()
        # the possibilities eliminated
        changed = 0
        # loop through the row
        for c in range(len(self.cells[r])):
            # make sure it doesn't flip itself
            if c != cc:
                # given a possibility, set all other columns in the row to 0 as well since two cells
                # on the same row cannot have the same value
                # this is done by column individually through each iteration of the loop
                flipped = self.flip(r, c, v, 0)
                # if the cell flipped
                if flipped > 0:
                    # the possibilities of that given cell r, c go down by 1
                    self.registry[r, c] -= 1
                    # if that cell now only has one possibility
                    if self.registry[r, c] == 1:
                        # the number of cells with singular possibilities increments
                        self.singular += 1
                # add number of cells changed
                changed += flipped
        return changed

    # checks the cell at current row rr at column c and eliminates possibilities
    def col(self, rr, c):
        # gets smallest value possible in the cell rr, c
        v = self.cells[rr, c].get_singular()
        # the possibilities eliminated
        changed = 0
        # loop through the column
        for r in range(len(self.cells[c])):
            if r != rr:
                # given a possibility, set all other rows in the column to 0 as well since two cells
                # on the same column cannot have the same value
                # this is done by row individually through each iteration of the loop
                flipped = self.flip(r, c, v, 0)
                # if the cell flipped
                if flipped > 0:
                    # the possibilities of that given cell r, c go down by 1
                    self.registry[r, c] -= 1
                    # if that cell now only has one possibility
                    if self.registry[r, c] == 1:
                        # the number of cells with singular possibilities increments
                        self.singular += 1
                # add number of cells changed
                changed += flipped
        return changed

    # checks each 3x3 box and eliminates possibilities
    # does basically the same thing as row and col, iterating through each box from left to right top to bottom
    def box(self, rr, cc):
        # the possibilities eliminated
        changed = 0
        # smallest possible value of the cell rr, cc
        v = self.cells[rr, cc].get_singular()
        # floor function but instead of one, its by factors of three
        r0 = 3 * int(rr / 3)
        c0 = 3 * int(cc / 3)
        # loops through the rows and columns
        for r in range(r0, r0 + 3):
            for c in range(c0, c0 + 3):
                # if the current cell is not the original cell
                if r != rr or c != cc:
                    # given a possibility, set all other cells in the box to 0 as well since two cells
                    # in the same box cannot have the same value
                    # this is done by cell individually through each iteration of the loop
                    flipped = self.flip(r, c, v, 0)
                    # if the cell flipped
                    if flipped > 0:
                        # the possibilities of that given cell r, c go down by 1
                        self.registry[r, c] -= 1
                        # if there are no possibilities for that cell then there is no solution
                        if self.registry[r, c] < 1:
                            return -1
                        # if that cell now only has one possibility
                        if self.registry[r, c] == 1:
                            self.singular += 1
                    # add number of cells changed
                    changed += flipped
        return changed

    # Eliminates all conflicts
    def parse(self):
        while True:
            changed = 0
            # loop through each cell
            for r in range(len(self.cells)):
                for c in range(len(self.cells)):
                    if self.registry[r, c] == 1:
                        # eliminate possibilites based on row, column, box
                        chg_r = self.row(r, c)
                        chg_c = self.col(r, c)
                        chg_b = self.box(r, c)
                        # if there are no possibilities in a row column or box, return False, this is a dead end
                        if chg_r == -1 or chg_c == -1 or chg_b == -1:
                            return False
                        changed += chg_r + chg_c + chg_b
            # once we have eliminated all possibilites, end the loop
            if changed == 0:
                # returns True, this is not a dead end
                return True

    @staticmethod
    # recursively solves the sudoku puzzle with given values
    def solve(given):
        # creates the 9x9 grid to write our solutions to
        solution = np.empty((9, 9), dtype=int)
        # create the grid to solve on
        grid = Grid(given)
        if not grid.parse():
            # this is a dead end
            return None
        # variables to help identify the cell with the least number of possibilities
        mr = -1  # the row of the cell with the least number of possibilties so far in the loop
        mc = -1  # the column of the cell with the least number of possibilties so far in the loop
        md = 10  # minimum number of possibilities so far in the loop that is not 1, 10 is above the max
        # we don't want cells with 1 possibility, because it's already part of the solution
        for r in range(len(grid.cells)):
            for c in range(len(grid.cells)):
                solution[r, c] = 0
                # if there is only one possibility
                if grid.registry[r, c] == 1:
                    # set the solution to that cell with one possibility ( + 1 because we want 1-9 instead of 0-8)
                    solution[r, c] = grid.cells[r, c].get_singular() + 1
                else:
                    # if the number of possibilities is less than the current minimum
                    if grid.registry[r, c] < md:
                        mr = r  # update minimum's row
                        mc = c  # update minimum's col
                        md = grid.registry[r, c]  # update the minimum
        # if we have 81 cells with only one possible number, then we have solved the puzzle
        if grid.singular == 81:
            # return the solution
            return solution
        # get the minimum cell that has more than one possibility, which from above, has the position:
        # column: mc, row: mr
        # loop through the potential values
        for d in range(9):
            # if d is a possibility, we set our solution to that possibility and run the solve recurisvely
            if grid.cells[mr, mc].values[d] != 0:
                # + 1 because we want numbers 1-9 not 0-8
                solution[mr, mc] = d + 1
                # run the recursion
                sol = Grid.solve(solution)
                # now our solution is complete (or it doesn't exist)
                if sol is not None:
                    # return the solution
                    return sol
        return None
