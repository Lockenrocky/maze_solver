import time
import random
from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running == True:
            self.redraw()
        print("window closed...")

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, start, end):
        self.x1 = start.x
        self.y1 = start.y
        self.x2 = end.x
        self.y2 = end.y
    
    def draw(self, canvas, fill_color="black"):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=fill_color, width=2)

class Cell():
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self._win = win
        self._visited = False

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        if self.has_left_wall:
            line = Line(Point(x1,y1), Point(x1,y2))
            self._win.draw_line(line)
        if self.has_left_wall == False:
            line = Line(Point(x1,y1), Point(x1,y2))
            self._win.draw_line(line, fill_color="white")            
        if self.has_right_wall:
            line = Line(Point(x2,y1), Point(x2,y2))
            self._win.draw_line(line)
        if self.has_right_wall == False:
            line = Line(Point(x2,y1), Point(x2,y2))
            self._win.draw_line(line, fill_color="white")            
        if self.has_top_wall:
            line = Line(Point(x1,y1), Point(x2,y1))
            self._win.draw_line(line)
        if self.has_top_wall == False:
            line = Line(Point(x1,y1), Point(x2,y1))
            self._win.draw_line(line, fill_color="white")
        if self.has_bottom_wall:
            line = Line(Point(x1,y2), Point(x2,y2))
            self._win.draw_line(line)
        if self.has_bottom_wall == False:
            line = Line(Point(x1,y2), Point(x2,y2))
            self._win.draw_line(line, fill_color="white")

    def draw_move(self, to_cell, undo=False):
        center1 = Point(abs(self._x1 + self._x2) // 2, abs(self._y1 + self._y2) // 2)
        center2 = Point(abs(to_cell._x1 + to_cell._x2) // 2, abs(to_cell._y1 + to_cell._y2) // 2) 
        line = Line(center1, center2)
        if undo:
            self._win.draw_line(line, fill_color="red")
        else:
            self._win.draw_line(line, fill_color="grey")

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        if seed != None:
            self.seed = random.seed(seed)
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._visited = []
        self._cells = []
        self._solved = False
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i ,j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _break_walls_r(self, i ,j):
        current_cell = self._cells[i][j]
        current_cell._visited = True
        while True:
            to_visit = []
            # top neighbor
            if j > 0 and self._cells[i][j-1]._visited == False:
                to_visit.append((i,j-1))
            # right neighbor
            if i < self._num_cols-1 and self._cells[i+1][j]._visited == False:
                to_visit.append((i+1,j))
            # bottom neighor
            if j < self._num_rows-1 and self._cells[i][j+1]._visited == False:
                to_visit.append((i, j+1))
            # left neighbor
            if i > 0 and self._cells[i-1][j]._visited == False:
                to_visit.append((i-1,j))
            if len(to_visit) == 0:
                self._draw_cell(i,j)
                return
            direction = random.choice(to_visit)
            choosen_cell = self._cells[direction[0]][direction[1]]
            # left
            if direction[0] < i:
                current_cell.has_left_wall = False
                choosen_cell.has_right_wall = False
            # right
            if direction[0] > i:
                current_cell.has_right_wall = False
                choosen_cell.has_left_wall = False            
            # top
            if direction[1] < j:
                current_cell.has_top_wall = False
                choosen_cell.has_bottom_wall = False               
            # bottom
            if direction[1] > j:
                current_cell.has_bottom_wall = False
                choosen_cell.has_top_wall = False               
            
            self._break_walls_r(direction[0], direction[1])               
            
    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j]._visited = False

    def solve(self):
        return self._solve_r(0,0)
    
    def _solve_r(self, i ,j):
        self._animate()
        self._cells[i][j]._visited = True
        current_cell = self._cells[i][j]
        if i == self._num_cols-1 and j == self._num_rows-1:
            self._solved = True
            return True
        while True:
        # top neighbor
            if j > 0 and self._cells[i][j-1]._visited == False and current_cell.has_top_wall == False and self._solved == False:
                current_cell.draw_move(self._cells[i][j-1])
                self._visited.append(current_cell)
                self._solve_r(i,j-1)          

            # right neighbor
            if i < self._num_cols-1 and self._cells[i+1][j]._visited == False and current_cell.has_right_wall == False and self._solved == False:
                current_cell.draw_move(self._cells[i+1][j])
                self._visited.append(current_cell)
                self._solve_r(i+1,j)

            # bottom neighor
            if j < self._num_rows-1 and self._cells[i][j+1]._visited == False and current_cell.has_bottom_wall == False and self._solved == False:
                current_cell.draw_move(self._cells[i][j+1])
                self._visited.append(current_cell)
                self._solve_r(i, j+1)              

            # left neighbor
            if i > 0 and self._cells[i-1][j]._visited == False and current_cell.has_left_wall == False and self._solved == False:
                current_cell.draw_move(self._cells[i-1][j])
                self._visited.append(current_cell)
                self._solve_r(i-1,j)
            
            if self._solved == False:
                current_cell.draw_move(self._visited.pop(), True)
                return False
            else:
                return True
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0,0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(self._num_cols-1, self._num_rows-1)

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)
