import numpy as np
import random
import math
from copy import deepcopy

obstaculo = "#"
atual = "\x1b[32mX\x1b[0m"
objetivo = "\x1b[34mO\x1b[0m"

class Maze:
    def __init__(self, lines, columns, cur=None, obstacle=None, cur_move=None) -> None:
        self.maze = np.empty((lines, columns), dtype= 'object')  
        self.lines, self.columns = (lines, columns)
        
        self.last_move = ['last', 1]
        self.cur_move = ['cur', 0]
        
        #ATUAL
        if cur is not None: #se já se tiver feito algum movimento
            self.cur_line, self.cur_col = cur
        else: #para iniciar o labirinto
            self.cur_line = self.lines - 1 
            self.cur_col = 0 
        self.maze[self.cur_line, self.cur_col] = atual
        
        #TARGET
        self.target_line = 0
        self.target_col = self.columns - 1
        self.maze[self.target_line, self.target_col] = objetivo
        #se obstacle != None gera-se obstaculos
        if isinstance(obstacle, list):
            self.generate_obstacles(obstacle)
            
        self.move_history = [self.copy()]
        
    def __str__(self) -> str:
        string = '+' + '-'*(2*self.columns - 1) + '+ \n'
        for line in self.maze:
            string += '|'
            for cell in line:
                if cell is None:
                    string += ' '
                else:
                    string += cell
                string += '|'
            string += '\n'
            string += '+' + '-'*(2*self.columns - 1) + '+ \n'
        return string
    
    def __eq__(self, other: object) -> bool:
        return np.array_equal(self.maze, other) 
    
    def __hash__(self):
        #permite usar o estado do labirinto em um conjunto (set)
        return hash(str([item for sublist in self.maze for item in sublist]))
    
    def copy(self):
        maze_copy = deepcopy(self)
        return maze_copy
    
    def is_solvable(self,line,col) -> bool:
        for i in range(self.lines):
            for j in range(self.columns):
                counter = 0

                if i == line and j == col:  # Skip checking the target cell
                    continue

                if i==0:
                    counter +=1
                if j==0:
                    counter +=1
                if i==self.lines-1:
                    counter +=1
                if j==self.columns-1:
                    counter +=1

                if i > 0 and (self.maze[i - 1][j] == obstaculo or (i - 1 == line and j == col)):  # Check above cell
                    counter += 1
                if j > 0 and (self.maze[i][j - 1] == obstaculo or (i == line and j - 1 == col)):  # Check left cell
                    counter += 1
                if i < self.lines - 1 and (self.maze[i + 1][j] == obstaculo or (i + 1 == line and j == col)):  # Check below cell
                    counter += 1
                if j < self.columns - 1 and (self.maze[i][j + 1] == obstaculo or (i == line and j + 1 == col)):  # Check right cell
                    counter += 1
                if counter > 2:
                    return False
        return True
    
    def generate_obstacles(self, obstacles: list) -> None:
        if len(obstacles) == 0:  
            list_lines = list(range(self.lines))
            list_cols = list(range(self.columns))
            for _ in range(min(self.columns - 1, self.lines - 1)): 
                line = random.choice(list_lines)
                col = random.choice(list_cols)

                if [line, col] != [self.target_line, self.target_col] and [line, col] != [self.cur_line, self.cur_col] and self.is_solvable(line,col):
                    self.maze[line, col] = obstaculo
        else: 
            for line, col in obstacles:
                self.maze[line, col] = obstaculo
    
    def children(self) -> list:
        functions = [self.up, self.down, self.left, self.right]
        children = []
        for function in functions:
            child = function()
            if child:
                child.move_history += [deepcopy(child)]
                children.append(child)
        return children
    
    def move(func):
        def wrapper(self):
            maze = self.copy()
            done = func(maze)  
            if done:
                return maze  
            else:
                return None  
        return wrapper
    
    # Funções de movimento
    @move
    def up(self) -> bool:
        if self.cur_line == 0 or self.maze[self.cur_line - 1, self.cur_col] not in {None, objetivo} or (self.maze[self.cur_line - 1, self.cur_col] == objetivo and np.count_nonzero(self.maze == None) > 0) or (self.cur_move[0] != 'up' and self.cur_move[1] == self.last_move[1]):
            return False

        self.maze[self.cur_line, self.cur_col] = "↑"
        self.maze[self.cur_line - 1, self.cur_col] = atual
        self.cur_line -= 1
        
        if self.cur_move[0] == 'up': self.cur_move[1] += 1
        else: 
            self.last_move = self.cur_move
            self.cur_move = ['up', 1]
        return True
    
    @move
    def down(self) -> bool:
        if self.cur_line == self.lines - 1 or self.maze[self.cur_line + 1, self.cur_col] not in {None, objetivo} or (self.maze[self.cur_line + 1, self.cur_col] == objetivo and np.count_nonzero(self.maze == None) > 0) or (self.cur_move[0] != 'down' and self.cur_move[1] == self.last_move[1]):
            return False

        self.maze[self.cur_line, self.cur_col] = '↓'
        self.maze[self.cur_line + 1, self.cur_col] = atual
        self.cur_line += 1
        
        if self.cur_move[0] == 'down': self.cur_move[1] += 1
        else: 
            self.last_move = self.cur_move
            self.cur_move = ['down', 1]
        return True
    
    @move
    def left(self) -> bool:
        if self.cur_col == 0 or self.maze[self.cur_line, self.cur_col - 1] not in {None, objetivo} or (self.maze[self.cur_line, self.cur_col - 1] == objetivo and np.count_nonzero(self.maze == None) > 0) or (self.cur_move[0] != 'left' and self.cur_move[1] == self.last_move[1]):
            return False

        self.maze[self.cur_line, self.cur_col] = '←'
        self.maze[self.cur_line, self.cur_col - 1] = atual
        self.cur_col -= 1
        
        if self.cur_move[0] == 'left': self.cur_move[1] += 1
        else: 
            self.last_move = self.cur_move
            self.cur_move = ['left', 1]
        return True
    
    @move
    def right(self) -> bool:
        if self.cur_col == self.columns - 1 or self.maze[self.cur_line, self.cur_col + 1] not in {None, objetivo} or (self.maze[self.cur_line, self.cur_col + 1] == objetivo and np.count_nonzero(self.maze == None) > 0) or (self.cur_move[0] != 'right' and self.cur_move[1] == self.last_move[1]):
            return False

        self.maze[self.cur_line, self.cur_col] = '→'
        self.maze[self.cur_line, self.cur_col + 1] = atual
        self.cur_col += 1
        
        if self.cur_move[0] == 'right': self.cur_move[1] += 1
        else: 
            self.last_move = self.cur_move
            self.cur_move = ['right', 1]
        return True
    
    def is_solved(self) -> bool: 
        return np.sum(self.maze == 0) == 0 and self.cur_line == self.target_line and self.cur_col == self.target_col

def print_sequence(node:Maze):
    if node is None:
        print('There is no solution')
        return
    print("Steps:", len(node.move_history) - 1)
    # prints the sequence of states
    for maze in node.move_history:
        print(maze)
        print()

# maze = Maze(4,4)
# print(maze)
# maze.children()
# maze = maze.children()[0]
# maze = maze.children()[0]
# maze = maze.children()[1]
# maze = maze.children()[2]
# for child in maze.children():
#     print(child)

