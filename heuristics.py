from Maze import Maze
from math import sqrt
import numpy as np

#Heuristicas

def distancia_euclidiana(maze:Maze) -> float:
    return sqrt((maze.cur_line - maze.target_line) ** 2 + (maze.cur_col - maze.target_col) ** 2)

def distancia_manhattan(maze:Maze) -> int:
    return abs(maze.target_line - maze.cur_line) + abs(maze.target_col - maze.cur_col)

def min_distance_from_zeros(maze:Maze) -> int:
    sum=0
    for i in range(maze.lines):
        for j in range(maze.columns):
            if maze.maze[i, j] == None: #celulas ainda nao visitadas
                    sum += abs(maze.target_line - i) + abs(maze.target_col - j)
    return sum

# maze = Maze(2,2)
# print(maze)
# print(distancia_manhattan(maze))
# print(distancia_euclidiana(maze))
# print(min_distance_from_zeros(maze))