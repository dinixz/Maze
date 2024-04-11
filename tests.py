from algorithms import *

import sys

# Save the original stdout
original_stdout = sys.stdout

# Redirect stdout to a file with UTF-8 encoding
with open('output.txt', 'w', encoding='utf-8') as f:
    sys.stdout = f
    
    
    lists_mazes = [easy_mazes, medium_mazes, hard_mazes]
    for i, list_mazes in enumerate(lists_mazes):
        print(i + 1)
        counter_manhattan = 0
        counter_euclidiana = 0
        empate = 0
        for i, maze in enumerate(list_mazes):
            inicio = time.time()
            a_star_search(maze, distancia_euclidiana)
            tempo_euclidiana = time.time() - inicio

            inicio = time.time()
            a_star_search(maze, distancia_manhattan)
            tempo_manhattan = time.time() - inicio

            diferença = tempo_euclidiana - tempo_manhattan
            if diferença > 0:
                counter_manhattan += 1
            elif diferença < 0:
                counter_euclidiana += 1
            else:
                empate += 1
        
        print('Euclidiana: ' , counter_euclidiana)
        print('Manhattan: ' , counter_manhattan)
        print('Empates: ' , empate)
        
sys.stdout = original_stdout