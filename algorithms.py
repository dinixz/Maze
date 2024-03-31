from Maze import Maze, print_sequence
from copy import deepcopy
from collections import deque
import numpy as np
import heapq
  
#DFS
def depth_first_search(initial_maze:Maze):
    stack = deque([initial_maze]) 
    visited = set()
    
    while stack:
        node = stack.pop() #get the last element that came in
        
        if node.is_solved():   
            return print_sequence(node)
        visited.add(node)
        children = node.children()
        for child in children:
            if child not in visited:
                stack.append(child)
                
    return print_sequence(None)

#Limited DFS
def depth_limited_search(initial_maze:Maze, depth_limit:int):
    stack = deque([(initial_maze, 0)])  
    visited = set()
    
    while stack:
        node, depth = stack.pop()
        if depth < depth_limit:
            if node.is_solved():
                return print_sequence(node)
            visited.add(node)
            children = node.children()
            for child in children:
                if child not in visited:
                    stack.append([child, depth + 1])
    return None


def iterative_deepening_search(initial_maze, depth_limit):
    depth=0
    result=None
    while result==None:
        if depth<depth_limit:
            depth+=1
        result = depth_limited_search(initial_maze,depth)
    return None

#BFS
def breadth_first_search(initial_maze):
    queue = deque([initial_maze])  
    
    while queue:
        maze = queue.popleft()   #primeiro elemento da fila (por ordem de chegada - FIFO)
        if maze.is_solved():   # ver se ja esta completo
            return print_sequence(maze)
        
        for child in maze.children():   # ver as children deste nó
            queue.append(child)        
    return None

#Greedy
def greedy_search(maze_inicial, heuristica):
    # Define um método de comparação para os mazes com base na função heurística fornecida
    setattr(maze_inicial, "__lt__", lambda self, other: heuristica(self) < heuristica(other))
    
    # Inicializa uma lista para armazenar os labirintos a serem explorados
    fila = [maze_inicial]
    # Inicializa um conjunto para manter o controle dos estados visitados e evitar revisitá-los
    visitados = set()
    
    while fila:
        # Retira o maze com o MENOR valor heurístico da fila de prioridade
        atual = heapq.heappop(fila)
        
        visitados.add(atual) #labirinto visitado
        
        if atual.is_solved(): #se o problema está resolvido
            return print_sequence(atual)
        
        # Gera os mazes filhos a partir do atual
        for filho in atual.children():
            if filho not in visitados:
                heapq.heappush(fila, filho)

    return None

def a_star_search(maze_inicial, heuristica):
        return greedy_search(maze_inicial, lambda hrst: heuristica(maze_inicial) + len(maze_inicial.move_history) - 1) #-1=estado inicial