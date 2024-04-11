from math import sqrt
import numpy as np
from Maze import *

#Heuristicas
def unsolvable(maze:Maze):
    directions = {up_symbol, down_symbol, left_symbol, right_symbol, atual, obstaculo}
    for line in range(maze.lines):
        for col in range(maze.columns):
            if maze.maze[line, col] is None:
                impossible = True
                # up
                if line != 0:
                    impossible = (impossible and maze.maze[line - 1, col] in directions)
                # down
                if line != maze.lines - 1:
                    impossible = (impossible and maze.maze[line + 1, col] in directions)
                # left
                if col != 0:
                    impossible = (impossible and maze.maze[line, col - 1] in directions)
                # right
                if col != maze.columns - 1:
                    impossible = (impossible and maze.maze[line, col + 1] in directions)
                if impossible: return True
    return False

def distancia_euclidiana(maze:Maze, coords=None) -> float:
    if coords is None:
        line = maze.cur_line
        col = maze.cur_col
    else: line, col = coords
    return sqrt((maze.target_line - line) ** 2 + (maze.target_col - col) ** 2)

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
                score += distancia_manhattan(maze, (line, column))
            # elif maze.maze[line, column] in {up_symbol, down_symbol, left_symbol, right_symbol}:
            #     score += distancia_manhattan(maze, (line, column))
    score += 3*np.count_nonzero(maze.maze == None)
    if unsolvable(maze):
        return float('inf')
    return score

def h2(maze:Maze) -> float:
    return distancia_euclidiana(maze) + distancia_manhattan(maze) +  2* np.count_nonzero(maze.maze == None)

# maze = Maze(3,3)
# maze = maze.up()
# maze = maze.up()
# maze = maze.right()
# maze = maze.down()
# maze = maze.down()
# maze = maze.right()
# print(h1(maze))

# maze2 = Maze(3,3)
# maze2 = maze2.right()
# maze2 = maze2.up()
# maze2 = maze2.up()
# maze2 = maze2.right()
# print(h1(maze2))