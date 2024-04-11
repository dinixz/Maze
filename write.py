from Maze import Maze
from heuristics import distancia_euclidiana, distancia_manhattan
from algorithms import *
import time

import sys

# Save the original stdout
original_stdout = sys.stdout

# Redirect stdout to a file with UTF-8 encoding
with open('output.txt', 'w', encoding='utf-8') as f:
    sys.stdout = f
    for i, maze in enumerate(easy_mazes):
        print('Maze ' + str(i))
        print(maze)
        
        inicio = time.time()
        final = greedy_search(maze, distancia_euclidiana)
        if final: 
            print('Euclidiana: ' + str(time.time()-inicio))
        print(final)

        inicio = time.time()
        final = greedy_search(maze, distancia_manhattan)
        if final: 
            print('Manhattan: ' + str(time.time()-inicio))
        print(final)
        
sys.stdout = original_stdout