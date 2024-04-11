from Maze import *
from algorithms import *

def possible_moves_player(state:Maze):
    return {'up': state.up(), 'down': state.down(), 'left': state.left(), 'right': state.right()}

def get_hint(state:Maze, final_state:Maze) -> str:
    '''
        Podiamos gerar o final_state desta forma:
            1- O jogador jogou e atualiza-se o estado
            2- Geramos logo o final_state usando o melhor algoritmo
            3- Quando o jogador quiser uma dica já não precisa de se gerar o final_state naquele momento, evitando esperas, basta passá-los para esta funçao
    '''
    hint = {up_symbol: 'up', down_symbol: 'down', left_symbol: 'left', right_symbol: 'right'}
    next_move = final_state.maze[state.cur_line, state.cur_col]
    return hint.get(next_move)
    