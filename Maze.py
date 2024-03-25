import numpy as np
import random
import math
from copy import deepcopy
from collections import deque

'''
    Maze é uma array numpy para ser mais eficiente que uma lista
    As entradas são:
        -1 -> obstáculos
        0 -> espaços livres
        1 -> espaços já percorridos
        2 -> meta a que temos de chegar
    O atributo cur_line e cur_col ao gerar o labirinto são a linha e coluna iniciais
    Depois do primeiro move são onde se situa o nosso "agente"
    A função generate_obstacles quando não são dadas as posições dos obstaculos por vezes gera obstaculos que impedem de haver solução para o labirinto
'''

class Maze:
    def __init__(self, maze: np.array, move_history=[], cur=None, obstacle=None) -> None:
        self.maze = deepcopy(maze)  #cópia da matriz do labirinto para evitar alterações inesperadas
        self.lines, self.columns = maze.shape  #número de linhas e colunas do labirinto
        self.move_history = [] + move_history + [self]  #registro dos movimentos realizados no labirinto
        
        #atualiza a posição atual 
        if cur is not None: #se já se tiver feito algum movimento
            self.cur_line, self.cur_col = cur
        else: #para iniciar o labirinto
            self.cur_line = self.lines - 1 
            self.cur_col = 0 
        self.maze[self.cur_line, self.cur_col] = 1  
        
        #posição de objetivo 
        self.target_line = 0
        self.target_col = self.columns - 1
        self.maze[self.target_line, self.target_col] = 2
        
        #se obstacle != None gera-se obstaculos
        if isinstance(obstacle, list):
            self.generate_obstacles(obstacle)
        
    def __str__(self) -> str:
        string = ''
        for line in self.maze:
            for cell in line:
                if cell == -1:
                    string += '#'
                else:
                    string += str(int(cell))
            string += '\n'
        return string
    
    def __eq__(self, other: object) -> bool:
        return np.array_equal(self.maze, other) 
    
    def __hash__(self):
        #permite usar o estado do labirinto em um conjunto (set)
        return hash(str([item for sublist in self.maze for item in sublist]))
    
    def is_solvable(self,line,col) -> bool:
        for i in range(self.lines):
            for j in range(self.columns):
                counter = 0

                if i == line and j == col:  # Skip checking the target cell
                    continue

                if i==0:
                    counter +=1
                if j==0:
                    counter +=1
                if i==self.lines-1:
                    counter +=1
                if j==self.columns-1:
                    counter +=1

                if i > 0 and (self.maze[i - 1][j] == -1 or (i - 1 == line and j == col)):  # Check above cell
                    counter += 1
                if j > 0 and (self.maze[i][j - 1] == -1 or (i == line and j - 1 == col)):  # Check left cell
                    counter += 1
                if i < self.lines - 1 and (self.maze[i + 1][j] == -1 or (i + 1 == line and j == col)):  # Check below cell
                    counter += 1
                if j < self.columns - 1 and (self.maze[i][j + 1] == -1 or (i == line and j + 1 == col)):  # Check right cell
                    counter += 1
                if counter > 2:
                    return False
        return True
    
    def generate_obstacles(self, obstacles: list) -> None:
        if len(obstacles) == 0:  #se não for dado nenhum obstaculo gera-se aleatórios (corre o risco de ser impossível encontrar soluçao)
            list_lines = list(range(self.lines))
            list_cols = list(range(self.columns))
            for _ in range(min(self.columns - 1, self.lines - 1)): #para não haver uma linha de obstaculos que divide a pos inicial da final
                line = random.choice(list_lines)
                col = random.choice(list_cols)
                # Verifica se o obstáculo não está nas posições do agente ou do objetivo
                #verifica se os obstaculos nao tornam o puzzle impossivel, todas as posicoes têm 2 saidas
                if [line, col] != [self.target_line, self.target_col] and [line, col] != [self.cur_line, self.cur_col] and self.is_solvable(line,col):
                    self.maze[line, col] = -1
        else:  #se obstáculos forem fornecidos, usa essas posições
            for line, col in obstacles:
                self.maze[line, col] = -1
    
   
    
    def children(self) -> list:
        # Gera os filhos possíveis do estado atual do labirinto
        functions = [self.up, self.down, self.left, self.right]  #lista de funções de movimento
        children = []
        for function in functions:
            child = function()  #aplica cada função de movimento
            if child:
                children.append(child)  #adiciona o filho se o movimento for válido
        return children
    
    def move(func):
    #decorador para lidar com movimentos    
        def wrapper(self):
            maze = Maze(self.maze, self.move_history, (self.cur_line, self.cur_col))  #cópia do labirinto
            done = func(maze)  #função de movimento
            if done:
                return maze  #retorna o labirinto modificado se o movimento for bem-sucedido
            else:
                return None  #retorna None se o movimento for inválido
        return wrapper
    
    # Funções de movimento
    @move
    def up(self) -> bool:
        # Verifica se o movimento para cima é válido
        if self.cur_line == 0 or self.maze[self.cur_line - 1, self.cur_col] in {-1, 1} or (self.maze[self.cur_line - 1, self.cur_col] == 2 and np.count_nonzero(self.maze == 0) > 0):
            return False
        # Move o agente para cima e atualiza a posição no labirinto
        self.maze[self.cur_line - 1, self.cur_col] = 1
        self.cur_line -= 1
        return True
    
    @move
    def down(self) -> bool:
        # Verifica se o movimento para baixo é válido
        if self.cur_line == self.lines - 1 or self.maze[self.cur_line + 1, self.cur_col] in {-1, 1} or (self.maze[self.cur_line + 1, self.cur_col] == 2 and np.count_nonzero(self.maze == 0) > 0):
            return False
        # Move o agente para baixo e atualiza a posição no labirinto
        self.maze[self.cur_line + 1, self.cur_col] = 1
        self.cur_line += 1
        return True
    
    @move
    def left(self) -> bool:
        # Verifica se o movimento para a esquerda é válido
        if self.cur_col == 0 or self.maze[self.cur_line, self.cur_col - 1] in {-1, 1} or (self.maze[self.cur_line, self.cur_col - 1] == 2 and np.count_nonzero(self.maze == 0) > 0):
            return False
        # Move o agente para a esquerda e atualiza a posição no labirinto
        self.maze[self.cur_line, self.cur_col - 1] = 1
        self.cur_col -= 1
        return True
    
    @move
    def right(self) -> bool:
        # Verifica se o movimento para a direita é válido
        if self.cur_col == self.columns - 1 or self.maze[self.cur_line, self.cur_col + 1] in {-1, 1} or (self.maze[self.cur_line, self.cur_col + 1] == 2 and np.count_nonzero(self.maze == 0) > 0):
            return False
        # Move o agente para a direita e atualiza a posição no labirinto
        self.maze[self.cur_line, self.cur_col + 1] = 1
        self.cur_col += 1
        return True
    
    def is_solved(self) -> bool:
    # Verifica se o labirinto foi resolvido (todas as posições visitadas e o objetivo alcançado)    
        return np.prod(self.maze) != 0 and self.cur_line == self.target_line and self.cur_col == self.target_col

def print_sequence(node:Maze):
    if node is None:
        print('There is no solution')
        return
    print("Steps:", len(node.move_history) - 1)
    # prints the sequence of states
    for maze in node.move_history:
        print(maze)
        print()


class TreeNode:
    def __init__(self, maze, parent=None):
        self.maze = maze
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
    

#DFS
def depth_first_search(initial_maze):
    root = TreeNode(initial_maze)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes
    visited = set([initial_maze])
    
    while queue:
        node = queue.pop()   # get first element in the queue
        maze=node.maze
        if maze.is_solved():   # check goal state
            return print_sequence(node.maze)
        
        for child in maze.children():
            #se nao esta visitado ent visitmos
            if child not in visited:
                # criar no usando o estdo novo encontrado
                child_node=TreeNode(maze=child, parent=node)
                #adicionar esse no aos filhos do meu no atual
                node.add_child(child_node)
                #po-lo na fila
                queue.append(child_node)
                visited.add(child)
            #se ja tiver sido visitado n vamos andar as voltas a criar arvore que ja existe antes
            

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


#Heuristicas

def heuristica1(maze): # Distância Euclidiana
    # Obtenção das coordenadas atuais do agente no labirinto
    x0 = maze.cur_line
    y0 = maze.cur_col
    # Inicialização do valor com infinito e a posição atual
    value = (float('inf'), (x0, y0))
    # Obtenção das coordenadas do alvo no labirinto
    x1 = maze.target_line
    y1 = maze.target_col
    
    # Verificação e cálculo da distância para baixo, se possível
    if x0 >= 0 and x0 < maze.lines - 1 and maze.maze[x0+1,y0]==0:
        dist = distancia_euleriana(x0 + 1, y0, x1, y1)
        if dist[0] < value[0]:
            value = dist
    # Verificação e cálculo da distância para cima, se possível
    elif x0 > 0 and x0 <= maze.lines - 1 and maze.maze[x0-1,y0]==0:
        dist = distancia_euleriana(x0 - 1, y0, x1, y1)
        if dist[0] < value[0]:
            value = dist
    
    # Verificação e cálculo da distância para direita, se possível
    if y0 >= 0 and y0 < maze.columns - 1 and maze.maze[x0,y0+1]==0:
        dist = distancia_euleriana(x0, y0 + 1, x1, y1)
        if dist[0] < value[0]:
            value = dist
    # Verificação e cálculo da distância para esquerda, se possível
    elif y0 > 0 and y0 <= maze.columns - 1 and maze.maze[x0,y0-1]==0:
        dist = value[0], distancia_euleriana(x0, y0 - 1, x1, y1)
        if dist[0] < value[0]:
            value = dist
    
    return value

def distancia_euleriana(x, y, z, w) -> float:
    # Cálculo da distância Euclidiana entre dois pontos
    return (math.sqrt((x - z) ** 2 + (y - w) ** 2), (x, y))


def heuristica2(maze): #distancia Manhattan (distancia usando apenas movimentos na matriz)
    x0=maze.cur_line
    y0=maze.cur_col
    value=(float('inf'),(x0,y0))
    x1=maze.target_line
    y1=maze.target_col
    # Verificação e cálculo da distância para baixo, se possível
    if x0 >= 0 and x0 < maze.lines - 1 and maze.maze[x0+1,y0]==0:
        dist = distancia_manhattan(x0 + 1, y0, x1, y1)
        if dist[0] < value[0]:
            value = dist
    # Verificação e cálculo da distância para cima, se possível
    elif x0 > 0 and x0 <= maze.lines - 1 and maze.maze[x0-1,y0]==0:
        dist = distancia_manhattan(x0 - 1, y0, x1, y1)
        if dist[0] < value[0]:
            value = dist
    
    # Verificação e cálculo da distância para direita, se possível
    if y0 >= 0 and y0 < maze.columns - 1 and maze.maze[x0,y0+1]==0:
        dist = distancia_manhattan(x0, y0 + 1, x1, y1)
        if dist[0] < value[0]:
            value = dist
    # Verificação e cálculo da distância para esquerda, se possível
    elif y0 > 0 and y0 <= maze.columns - 1 and maze.maze[x0,y0-1]==0:
        dist = value[0], distancia_manhattan(x0, y0 - 1, x1, y1)
        if dist[0] < value[0]:
            value = dist
    return value

def distancia_manhattan(x,y,z,w) -> int:
    # Calcula a distância de Manhattan entre a posição atual e o objetivo    
        return (abs(z - x) + abs(w - y),(x,y))


#Interface jogdor usar com ajuda de AI e AI resolver sozinha



#Testar código
maze = Maze(np.zeros((4,4)), [], obstacle= [])

maze_teste=Maze(np.zeros((4,4)),[],obstacle=[(0,0), (1,3), (0,1)])
#print(maze_teste)

#depth_limited_search(maze_teste,12)
#iterative_deepening_search(maze_teste, 14)
#breadth_first_search(maze_teste)

maze_teste_heuristicas=Maze(np.zeros((4,4)),[],(3,0),obstacle=[(0,0), (1,3), (0,1)])
print(maze_teste_heuristicas)

print(heuristica2(maze_teste_heuristicas))

