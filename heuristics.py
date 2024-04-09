from math import sqrt
import numpy as np
from Maze import *

#Heuristicas
# def unsolvable(maze:Maze):
#     for line in range(maze.lines):
#         for col in range(maze.columns):
#             exit = 0
#             up
#             if line != 0:
#                 if maze.maze[line -1, col] is None:
#                     exit += 1
#             down
#             if line != maze.lines - 1:
#                 if maze.maze[line + 1, col] is None:
#                     exit += 1
#             left
#             if col != 0:
#                 if maze.maze[line, col -1] is None:
#                     exit += 1
#             right
#             if col != maze.columns - 1:
#                 if maze.maze[line, col + 1] is None:
#                     exit += 1
#             if exit < 2:
#                 return True
#     return False

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
    score -= maze.cur_move[1]
    for line in range(maze.lines):
        for column in range(maze.columns):
            if maze.maze[line, column] is None:
                score += distancia_manhattan(maze, (line, column)) 
            elif maze.maze[line, column] in {up_symbol, down_symbol, left_symbol, right_symbol}:
                score -= distancia_manhattan(maze, (line, column))
    # score += np.count_nonzero(maze.maze == None) - np.count_nonzero((maze.maze == up_symbol) | (maze.maze == down_symbol) | (maze.maze == left_symbol) | (maze.maze == right_symbol))
    # if unsolvable(maze):
    #     score += 10**6
    return score

def h2(maze:Maze):
    return -distancia_manhattan(maze) - distancia_euclidiana(maze) + np.count_nonzero(maze.maze == None)

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