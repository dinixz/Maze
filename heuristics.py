from math import sqrt
import numpy as np
from Maze import *

#Heuristicas
def distancia_euclidiana(maze:Maze, coords=None) -> float:
    if coords is None:
        line = maze.cur_line
        col = maze.cur_col
    else: line, col = coords
    return sqrt((maze.cur_line - line) ** 2 + (maze.cur_col - col) ** 2)

def distancia_manhattan(maze:Maze, coords=None) -> int:
    if coords is None:
        line = maze.cur_line
        col = maze.cur_col
    else: line, col = coords
    return abs(maze.target_line - line) + abs(maze.target_col - col)

def min_distance_from_zeros(maze) -> int:
    sum=0
    for i in range(maze.lines):
        for j in range(maze.columns):
            if maze.maze[i, j] == None: #celulas ainda nao visitadas
                    sum += abs(maze.target_line - i) + abs(maze.target_col - j)
    return sum

def h1(maze:Maze):
    score = 0
    for line in range(maze.lines):
        for column in range(maze.columns):
            if maze.maze[line, column] is None:
                score -= distancia_euclidiana(maze, (line, column)) 
            elif maze.maze[line, column] in {up_symbol, down_symbol, left_symbol, right_symbol}:
                score += distancia_euclidiana(maze, (line, column))
    score += np.count_nonzero(maze.maze == None) - np.count_nonzero((maze.maze == up_symbol) | (maze.maze == down_symbol) | (maze.maze == left_symbol) | (maze.maze == right_symbol))
    return score

# maze = Maze(5,5)
# l=[]
# maze = maze.right()
# l += maze.children()
# maze = maze.right()
# l += maze.children()
# maze = maze.right()
# l += maze.children()
# maze = maze.right()
# l += maze.children()
# maze = maze.up()
# l += maze.children()

# for i in l:
#     print(i)
#     print(h1(i))
#     print('-----------------------------------------')