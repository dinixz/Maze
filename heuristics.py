from Maze import Maze
from math import sqrt
import numpy as np

#Heuristicas

def distancia_euclidiana(maze:Maze) -> float:
    return sqrt((maze.cur_line - maze.target_line) ** 2 + (maze.cur_col - maze.target_col) ** 2)

def distancia_manhattan(maze:Maze) -> int:
        return abs(maze.target_line - maze.cur_line) + abs(maze.target_col - maze.cur_col)

# maze = Maze(np.zeros((2,2)), [])
# print(maze)
# print(maze.cur_line, maze.cur_col)
# print(distancia_manhattan(maze))