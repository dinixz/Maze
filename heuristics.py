from Maze import *
from math import sqrt


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
    return (sqrt((x - z) ** 2 + (y - w) ** 2), (x, y))


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
