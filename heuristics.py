from math import sqrt
from Maze import Maze

def distancia_euclidiana(maze:Maze) -> float:
    return sqrt((maze.target_line - maze.cur_line) ** 2 + (maze.target_col - maze.cur_col) ** 2)

def distancia_manhattan(maze:Maze) -> int:
    return abs(maze.target_line - maze.cur_line) + abs(maze.target_col - maze.cur_col)
