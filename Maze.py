import numpy as np
import random, time
from copy import deepcopy

obstaculo = "#"
atual = "\x1b[32mX\x1b[0m"
objetivo = "\x1b[34mO\x1b[0m"
up_symbol = "↑"
down_symbol = '↓'
left_symbol = '←'
right_symbol = '→'

class Maze:
    def __init__(self, lines:int, columns:int, obstacle=None, move_history=[]) -> None:
        self.maze = np.empty((lines, columns), dtype= 'object') 
        self.lines, self.columns = (lines, columns)
        
        self.last_move = ['last', float('inf')]
        self.cur_move = ['cur', float('-inf')]
        
        #ATUAL
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
            
        self.move_history = [self]
        
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
    
    def __eq__(self, other:object) -> bool:
        return np.array_equal(self.maze, other) 
    
    def __hash__(self):
        #permite usar o estado do labirinto em um conjunto (set)
        return hash(str([item for sublist in self.maze for item in sublist]))
    
    def copy(self):
        return deepcopy(self)
    
    def is_solvable(self, line:int, col:int) -> bool:
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
    
    def generate_obstacles(self, obstacles:list) -> None:
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
                children.append(child)
        return children
    
    # Funções de movimento
    def up(self):
        copied = self.copy()
        if (copied.cur_line == 0 or 
            copied.maze[copied.cur_line - 1, copied.cur_col] not in {None, objetivo} or 
            (copied.maze[copied.cur_line - 1, copied.cur_col] == objetivo and np.count_nonzero(copied.maze == None) > 0) or 
            (copied.cur_move[0] != 'up' and copied.cur_move[1] == copied.last_move[1])):
            return None
        else:
            copied.maze[copied.cur_line, copied.cur_col] = up_symbol
            copied.maze[copied.cur_line - 1, copied.cur_col] = atual
            copied.cur_line -= 1
            
            if copied.cur_move[0] == 'up': copied.cur_move[1] += 1
            else: 
                copied.last_move = copied.cur_move
                copied.cur_move = ['up', 1]
                
            copied.move_history.append(self.maze)
        return copied
    
    def down(self):
        copied = self.copy()
        if (copied.cur_line == copied.lines - 1 or 
            copied.maze[copied.cur_line + 1, copied.cur_col] not in {None, objetivo} or 
            (copied.maze[copied.cur_line + 1, copied.cur_col] == objetivo and np.count_nonzero(copied.maze == None) > 0) or 
            (copied.cur_move[0] != 'down' and copied.cur_move[1] == copied.last_move[1])):
            return None
        else:
            copied.maze[copied.cur_line, copied.cur_col] = down_symbol
            copied.maze[copied.cur_line + 1, copied.cur_col] = atual
            copied.cur_line += 1
            
            if copied.cur_move[0] == 'down': copied.cur_move[1] += 1
            else: 
                copied.last_move = copied.cur_move
                copied.cur_move = ['down', 1]
                
            copied.move_history.append(self.maze)
        return copied
    
    def left(self):
        copied = self.copy()
        if (copied.cur_col == 0 or 
            copied.maze[copied.cur_line, copied.cur_col - 1] not in {None, objetivo} or 
            (copied.maze[copied.cur_line, copied.cur_col - 1] == objetivo and np.count_nonzero(copied.maze == None) > 0) or 
            (copied.cur_move[0] != 'left' and copied.cur_move[1] == copied.last_move[1])):
            return None
        else:
            copied.maze[copied.cur_line, copied.cur_col] = left_symbol
            copied.maze[copied.cur_line, copied.cur_col - 1] = atual
            copied.cur_col -= 1
            
            if copied.cur_move[0] == 'left': copied.cur_move[1] += 1
            else: 
                copied.last_move = copied.cur_move
                copied.cur_move = ['left', 1]
                
            copied.move_history.append(self.maze)
        return copied
    
    def right(self):
        copied = self.copy()
        if (copied.cur_col == copied.columns - 1 or 
            copied.maze[copied.cur_line, copied.cur_col + 1] not in {None, objetivo} or 
            (copied.maze[copied.cur_line, copied.cur_col + 1] == objetivo and np.count_nonzero(copied.maze == None) > 0) or 
            (copied.cur_move[0] != 'right' and copied.cur_move[1] == copied.last_move[1])):
            return None
        else:
            copied.maze[copied.cur_line, copied.cur_col] = right_symbol
            copied.maze[copied.cur_line, copied.cur_col + 1] = atual
            copied.cur_col += 1
            
            if copied.cur_move[0] == 'right': copied.cur_move[1] += 1
            else: 
                copied.last_move = copied.cur_move
                copied.cur_move = ['right', 1]
                
            copied.move_history.append(self.maze)
        return copied
    
    def is_solved(self) -> bool: 
        return np.count_nonzero(self.maze == None) == 0 and self.cur_line == self.target_line and self.cur_col == self.target_col

def print_sequence(node=None):
    if node is None:
        print('There is no solution')
        return
    print("Steps:", len(node.move_history) - 1)
    # prints the sequence of states
    for maze in node.move_history:
        print(maze)

