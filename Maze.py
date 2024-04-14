import numpy as np
from copy import copy, deepcopy

obstaculo = "#"
cur = "X"
objetivo = "O"
up_symbol = "↑"
down_symbol = '↓'
left_symbol = '←'
right_symbol = '→'

class Maze:
    def __init__(self, lines:int, columns:int, obstacle=None, array=None) -> None:
        #se um array for fornecido, inicializa o labirinto com esse array, caso contrário, inicializa um labirinto vazio
        if not array is None:
            self.maze = array
            self.lines, self.columns = self.maze.shape
        else:
            self.maze = np.empty((lines, columns), dtype= 'object') 
            self.lines, self.columns = (lines, columns)
            
            #ATUAL
            self.cur_line = self.lines - 1 
            self.cur_col = 0 
            self.maze[self.cur_line, self.cur_col] = cur
            
            #TARGET
            self.target_line = 0
            self.target_col = self.columns - 1
            self.maze[self.target_line, self.target_col] = objetivo
        
        #historico dos movimentos
        self.last_move = ['last', float('inf')]
        self.cur_move = ['cur', float('-inf')]
        
        #se obstacle != None gera-se obstaculos
        if isinstance(obstacle, list):
            self.generate_obstacles(obstacle)
            
        self.move_history = [copy(self.maze)]
        
    def __str__(self) -> str:
        string = '+' + '-'*(2*self.columns - 1) + '+ \n'
        for line in self.maze:
            string += '|'
            for cell in line:
                if cell is None:
                    string += ' '
                else:
                    string += cell
                string += '|'
            string += '\n'
            string += '+' + '-'*(2*self.columns - 1) + '+ \n'
        return string
    
    def __eq__(self, other:object) -> bool:
        return np.array_equal(self.maze, other) 
    
    def __hash__(self):
        #permite usar o estado do labirinto em um conjunto (set)
        return hash(str([item for sublist in self.maze for item in sublist]))
    
    def copy(self):
        return deepcopy(self)

    def generate_obstacles(self, obstacles:list) -> None:
        for line, col in obstacles:
            self.maze[line, col] = obstaculo

    def children(self) -> list:
        functions = [self.up, self.down, self.left, self.right]
        children = []
        for function in functions:
            child = function()
            if child:
                children.append(child)
        return children
    
    # Funções de movimento
    def up(self):
        copied = self.copy()
        
        if (copied.cur_line == 0 or #na barreira superior
            copied.maze[copied.cur_line - 1, copied.cur_col] not in {None, objetivo} or #se a casa acima nao for casa válida
            (copied.maze[copied.cur_line - 1, copied.cur_col] == objetivo and np.count_nonzero(copied.maze == None) > 0) or #se tentar chegar ao target mesmo tendo casas nao visitadas
            (copied.cur_move[0] != 'up' and copied.cur_move[1] == copied.last_move[1])): #se a jogada anterior tiver o mesmo comprimento
            return None
        
        else:
            copied.maze[copied.cur_line, copied.cur_col] = up_symbol
            copied.maze[copied.cur_line - 1, copied.cur_col] = cur
            copied.cur_line -= 1
            
            if copied.cur_move[0] == 'up': #se o movimento anterior for igual ao atual
                copied.cur_move[1] += 1 
            else: #mudança de direção
                copied.last_move = copied.cur_move
                copied.cur_move = ['up', 1]
                
            copied.move_history.append(copy(copied.maze))
        return copied
    
    def down(self):
        copied = self.copy()
        if (copied.cur_line == copied.lines - 1 or #na barreira inferior
            copied.maze[copied.cur_line + 1, copied.cur_col] not in {None, objetivo} or #se a casa abaixo nao for casa válida
            (copied.maze[copied.cur_line + 1, copied.cur_col] == objetivo and np.count_nonzero(copied.maze == None) > 0) or #se tentar chegar ao target mesmo tendo casas nao visitadas
            (copied.cur_move[0] != 'down' and copied.cur_move[1] == copied.last_move[1])): #se a jogada anterior tiver o mesmo comprimento
            return None
        else:
            copied.maze[copied.cur_line, copied.cur_col] = down_symbol
            copied.maze[copied.cur_line + 1, copied.cur_col] = cur
            copied.cur_line += 1
            
            if copied.cur_move[0] == 'down': #se o movimento anterior for igual ao atual
                copied.cur_move[1] += 1 
            else: #mudança de direção
                copied.last_move = copied.cur_move
                copied.cur_move = ['down', 1]
                
            copied.move_history.append(copy(copied.maze))
        return copied
    
    def left(self):
        copied = self.copy()
        if (copied.cur_col == 0 or #na barreira lateral
            copied.maze[copied.cur_line, copied.cur_col - 1] not in {None, objetivo} or #se a casa esquerda nao for casa válida
            (copied.maze[copied.cur_line, copied.cur_col - 1] == objetivo and np.count_nonzero(copied.maze == None) > 0) or #se tentar chegar ao target mesmo tendo casas nao visitadas
            (copied.cur_move[0] != 'left' and copied.cur_move[1] == copied.last_move[1])): #se a jogada anterior tiver o mesmo comprimento
            return None
        else:
            copied.maze[copied.cur_line, copied.cur_col] = left_symbol
            copied.maze[copied.cur_line, copied.cur_col - 1] = cur
            copied.cur_col -= 1
            
            if copied.cur_move[0] == 'left': #se o movimento anterior for igual ao atual
                copied.cur_move[1] += 1
            else: #mudança de direção
                copied.last_move = copied.cur_move
                copied.cur_move = ['left', 1]
                
            copied.move_history.append(copy(copied.maze))
        return copied
    
    def right(self):
        copied = self.copy()
        if (copied.cur_col == copied.columns - 1 or #na barreira lateral
            copied.maze[copied.cur_line, copied.cur_col + 1] not in {None, objetivo} or #se a casa direita nao for casa válida
            (copied.maze[copied.cur_line, copied.cur_col + 1] == objetivo and np.count_nonzero(copied.maze == None) > 0) or #se tentar chegar ao target mesmo tendo casas nao visitadas
            (copied.cur_move[0] != 'right' and copied.cur_move[1] == copied.last_move[1])): #se a jogada anterior tiver o mesmo comprimento
            return None
        else:
            copied.maze[copied.cur_line, copied.cur_col] = right_symbol
            copied.maze[copied.cur_line, copied.cur_col + 1] = cur
            copied.cur_col += 1
            
            if copied.cur_move[0] == 'right': #se o movimento anterior for igual ao atual
                copied.cur_move[1] += 1
            else: #mudança de direção
                copied.last_move = copied.cur_move
                copied.cur_move = ['right', 1]
                
            copied.move_history.append(copy(copied.maze))
        return copied
    
    def is_solved(self) -> bool: 
        return np.count_nonzero(self.maze == None) == 0 and self.cur_line == self.target_line and self.cur_col == self.target_col

def print_sequence(node=None) -> None:
    if node is None:
        print('There is no solution')
        
    else:
        print("Steps: ", len(node.move_history) - 1)
        # prints the sequence of states
        for maze in node.move_history:
            print(Maze(maze.shape[0], maze.shape[1], array=maze))