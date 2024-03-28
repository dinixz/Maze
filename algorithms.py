from Maze import Maze, print_sequence
from copy import deepcopy
from collections import deque
import numpy as np
  
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
