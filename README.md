#Sudoku-Solver
This is a recursive Sudoku solver that can solve any valid Sudoku puzzle in less than a second

### Dependencies:
```
import os
import numpy as np
from selenium import webdriver
from tkinter import *
from tkinter import ttk
```
### File Overview:
Big picture overview of all the files:  
```grid.py```: Contains the grid and does most of the solving  
```solver.py```: Contains the GUI and initializes the grid  
```web.py```: Scrapes a puzzle from online  
### Controls:
```Clear```: Clears the puzzle  
```Solve```: Solves the puzzle  
```Web Sudoku```: Loads a random puzzle from websudoku.com  
```Input```: Simply input numbers into each cell in the Grid  
```Output```: The Grid outputs the solution, with given numbers as black and all other numbers as red.
If a solution is not found or the puzzle is invalid, the Grid will append all non-numeric cells with a red X.
Please note that if there are multiple solutions to a puzzle, the program will only output one.

### Error handling and known Errors:
1. You MUST have a google chrome driver as an environment variable named, by default ```CHROME```.
If you wish to have a driver with a different name, change ```line 12``` in ```web.py``` to:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```driver_name = '<driver name>'```  
Note if you do not do this, there will be an error
2. Invalid puzzles or inputs are handled by printing red X's

### Future plans
1. Determine number of solutions to a puzzle
2. Make sudoku puzzles with the program
