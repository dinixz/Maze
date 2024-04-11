from Maze import Maze, print_sequence
from collections import deque
import heapq
from heuristics import distancia_euclidiana, distancia_manhattan
import time

easy_mazes = [
    Maze(3,3),
    Maze(6,6, obstacle= [(0,0), (0,1), (0,2)]),
    Maze(6,6, obstacle= [(3,1), (3,2), (1,5)]),
    Maze(6,6, obstacle= [(4,1), (5,1), (1,3)]),
    Maze(6,6, obstacle= [(2,2), (4,3), (5,3)]),
    Maze(6,6, obstacle= [(0,4)]),
    Maze(6,6, obstacle= [(3,1), (4,3), (4,4)])
]

medium_mazes = [
    Maze(5,8, obstacle= [(2,0), (3,0), (0,6), (1,6)]),
    Maze(5,8, obstacle= [(1,1), (2,1), (4,6), (4,7)]),
    Maze(5,8, obstacle= [(0,0), (0,1), (0,2), (4,1)]),
    Maze(5,8, obstacle= [(0,0), (0,1), (4,6), (4,7)]),
    Maze(5,8, obstacle= [(0,6), (1,6), (2,4), (3,4)]),
    Maze(5,8, obstacle= [(0,2), (1,2), (2,4), (3,4)]),
    Maze(5,8, obstacle= [(1,3), (1,4), (1,5), (3,4)]),
    Maze(5,8, obstacle= [(0,2), (0,3)])
]

hard_mazes = [
    Maze(7,7, obstacle= [(0,3), (1,1)]),
    Maze(7,7, obstacle= [(6,1), (5,3), (3,3), (3,4)]),
    Maze(7,7, obstacle= [(2,0), (2,1), (5,0), (5,1)]),
    Maze(7,7, obstacle= [(2,0), (3,0), (3,2), (4,2)]),
    Maze(7,7, obstacle= [(2,5), (3,3), (6,5), (6,6)]),
    Maze(7,7, obstacle= [(1,1), (1,2), (3,3), (4,1)]),
    Maze(7,7, obstacle= [(3,3), (4,3), (3,6), (4,6)]),
    Maze(7,7, obstacle= [(4,1), (4,2), (5,6), (6,6)]),
    Maze(7,7, obstacle= [(3,1), (4,1), (3,6), (4,6)]),
    Maze(7,7, obstacle= [(6,1), (4,2), (4,4), (3,4)]),
    Maze(7,7, obstacle= [(4,2), (5,2), (4,5), (5,5)]),
    Maze(7,7, obstacle= [(6,1), (6,2), (1,6), (2,4)])
]

#DFS
def depth_first_search(initial_maze:Maze):
    stack = deque([initial_maze]) 
    visited = set()
    while stack:
        node = stack.pop() #get the last element that came in
        if node.is_solved():   
            return node
        visited.add(node)
        children = node.children()
        for child in children:
            if child not in visited:
                stack.append(child)
                
    return None

#Limited DFS
def depth_limited_search(initial_maze:Maze, depth_limit:int):
    stack = deque([(initial_maze, 0)])  
    visited = set()
    while stack:
        node, depth = stack.pop()
        if depth < depth_limit:
            if node.is_solved():
                return node
            visited.add(node)
            children = node.children()
            for child in children:
                if child not in visited:
                    stack.append([child, depth + 1])
        else: break
    return None

#Iterative Deepening search
def iterative_deepening_search(initial_maze, depth_limit):
    for i in range(depth_limit):
        result = depth_limited_search(initial_maze, i)
        if result:
            return result
    return None

#BFS
def breadth_first_search(initial_maze):
    queue = deque([initial_maze])  
    while queue:
        maze = queue.popleft()   #primeiro elemento da fila (por ordem de chegada - FIFO)
        if maze.is_solved(): 
            return maze
        for child in maze.children():   # ver as children deste nó
            queue.append(child)        
    return None

#Greedy
def greedy_search(initial_maze:Maze, heuristica):
    setattr(Maze, "__lt__", lambda self, other: heuristica(self) < heuristica(other)) # Define um método de comparação para os mazes com base na função heurística fornecida
    priority_queue = [initial_maze]
    visited = set()
    while priority_queue:
        atual = heapq.heappop(priority_queue) 
        if atual.is_solved(): 
            return atual
        visited.add(atual) #labirinto visitado
        children = atual.children()
        for child in children:
            if child not in visited:
                heapq.heappush(priority_queue, child)
    return None


def a_star_search(maze_inicial, heuristica):
        return greedy_search(maze_inicial, lambda hrst: heuristica(maze_inicial) + len(maze_inicial.move_history)) #-1=estado inicial

def  weighted_a_star_search(maze_inicial, heuristica, w):
        return greedy_search(maze_inicial, lambda hrst: w*heuristica(maze_inicial) + len(maze_inicial.move_history) - 1)