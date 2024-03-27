from Maze import Maze, print_sequence
from copy import deepcopy
from collections import deque
import numpy as np

class TreeNode:
    def __init__(self, maze, parent=None):
        self.maze = maze
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
    
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
def depth_limited_search(initial_maze, depth_limit):
    root = TreeNode(initial_maze)   # create the root node in the search tree
    queue = deque([(root,0)])   # initialize the queue to store the nodes
    visited = set([initial_maze])
    
    while queue:
        tuple = queue.pop()# get first element in the queue
        if tuple[1]>depth_limit:
            return None
        else:
            node=tuple[0]
            maze=node.maze
            if maze.is_solved():   #ver se ja esta resolvido
                return maze
        
            for child in maze.children():
            #se nao esta visitado ent visitmos
                if child not in visited:
                # criar no usando o estdo novo encontrado
                    child_node=TreeNode(maze=child, parent=node)
                #adicionar esse no aos filhos do meu no atual
                    node.add_child(child_node)
                #po-lo na fila
                    queue.append((child_node,tuple[1]+1))
                    visited.add(child)
            #se ja tiver sido visitado n vamos andar as voltas a criar arvore que ja existe antes
    return None

def depth_limited_search2(initial_maze:Maze, depth_limit:int): #acho que está melhor (????)
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
    return (print_sequence(result), depth)

#BFS
def breadth_first_search(initial_maze):
    root = TreeNode(initial_maze)  
    queue = deque([root])  
    
    while queue:
        node = queue.popleft()   #primeiro elemento da fila (por ordem de chegada - FIFO)
        maze=node.maze
        if maze.is_solved():   # ver se ja esta completo
            return print_sequence(maze)
        
        for child in maze.children():   # ver as children deste nó
            # criar um no novo encontrado
            child_node=TreeNode(maze=child, parent=node)
            #adicionar esse no aos filhos do meu no atual
            node.add_child(child_node)
            #po-lo na fila
            queue.append(child_node)        
    return None
