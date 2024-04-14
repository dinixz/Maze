import pygame, sys, random, time
from algorithms import *
from game import *

COR_PAREDE = (34, 139, 34) 
COR_CIRCLE = (34, 139, 34)
COR_FUNDO = (0, 0, 0)  
COR_OBSTACULO = (50, 50, 50)  
COR_ATUAL = (200, 50, 50)  
COR_OBJETIVO = (0, 0, 255)  
COR_POSITION = (255, 255, 10) 
COR_BOTAO = (255, 255, 90) 
COR_LETRA = (50, 50, 50) 

pygame.init()

# carregar as imagens usadas
pygame_player = pygame.image.load('images/pacman.png')
pygame_end = pygame.image.load('images/end.png')
pygame_barrier = pygame.image.load('images/barrier.png')
pygame_return = pygame.image.load('images/return.png')
pygame_background = pygame.image.load('images/geometric.jpg')
pygame_hint = pygame.image.load('images/hint.png')
pygame_retry = pygame.image.load('images/retry.png')

# dimensões do simbolo de return
return_symbol = pygame.transform.scale(pygame_return, (50,50))
hint_symbol = pygame.transform.scale(pygame_hint, (75,75))
retry_symbol = pygame.transform.scale(pygame_retry, (50,50))

# janela toda
janela_size = (1000, 700) 
janela = pygame.display.set_mode(janela_size)

# fontes
button_font = pygame.font.SysFont("Arial", 30)
title_font = pygame.font.Font('freesansbold.ttf' ,40)

# botões
botao_player = pygame.Rect(400 , 300 , 150, 55)
botao_ia = pygame.Rect(400, 375, 150, 55)

botao_facil = pygame.Rect(400 , 300 , 150, 55)
botao_medio = pygame.Rect(400, 375, 150, 55)
botao_dificil = pygame.Rect(400, 450, 150, 55)

botao_hint = hint_symbol.get_rect() #cria um retangulo para conter a imagem
botao_hint.center = (950,625) #posiçao na janela
botao_retry = retry_symbol.get_rect() #cria um retangulo para conter a imagem
botao_retry.center = (950, 50) #posiçao na janela
botao_return = return_symbol.get_rect() #cria um retangulo para conter a imagem
botao_return.center = (50,50) #posiçao na janela

def seta(tela, cell_size, linha, coluna, num) -> None: #0-up 1-left 2-down 3-right
    superficie = pygame.Surface((cell_size, cell_size)) #cria lugar da seta
    
    pygame.draw.polygon(superficie, (255, 0, 0), [[cell_size//2.1, cell_size//4], [cell_size//3.4, cell_size//2],[cell_size//1.5, cell_size//2]]) #triangulo da seta
    pygame.draw.rect(superficie, (255, 0, 0), (cell_size//2.54 , cell_size//2.5, cell_size//5, cell_size //2.7)) #retangulo da seta
    angulo_rotacao = 90  #rotaçao da seta
    superficie_rotacionada = pygame.transform.rotate(superficie, angulo_rotacao*num) #roda a seta

    tela.blit(superficie_rotacionada,( cell_size*coluna, cell_size*linha)) #desenha a seta

def draw_mode() -> None: # escolha do modo de jogo
    janela.blit(pygame_background, (0,0)) # mete o background

    # textos dos botões
    texto_player = button_font.render("PLAYER", True, COR_LETRA)
    texto_ia = button_font.render("IA", True, COR_LETRA)

    # retângulos dos botões
    pygame.draw.rect(janela, COR_BOTAO, botao_player, border_radius=10)
    pygame.draw.rect(janela, COR_BOTAO, botao_ia, border_radius=10)

    # obtém os retângulos dos textos para centralizá-los
    player_rect = texto_player.get_rect(center=botao_player.center)
    ia_rect = texto_ia.get_rect(center=botao_ia.center)

    # desenha os botões e centraliza o texto
    janela.blit(texto_player, player_rect)
    janela.blit(texto_ia, ia_rect)
    
    # título
    text = title_font.render("UNEQUAL MAZE THE CHALLENGE", True, (112, 129, 145))
    janela.blit(text, (150, 100))
    
    pygame.display.flip()

def draw_menu() -> None: # escolha da dificuldade do maze
    janela.blit(pygame_background, (0,0)) # mete o background

    # textos
    texto_facil = button_font.render("FÁCIL", True, COR_LETRA)
    texto_medio = button_font.render("MÉDIO", True, COR_LETRA)
    texto_dificil = button_font.render("DIFÍCIL", True, COR_LETRA)

    # retangulos dos botões
    pygame.draw.rect(janela, COR_BOTAO, botao_facil, border_radius=10)
    pygame.draw.rect(janela, COR_BOTAO, botao_medio, border_radius=10)
    pygame.draw.rect(janela, COR_BOTAO, botao_dificil, border_radius=10)

    # desenha os botões e centraliza o texto
    facil_rect = texto_facil.get_rect(center=botao_facil.center)
    medio_rect = texto_medio.get_rect(center=botao_medio.center)
    dificil_rect = texto_dificil.get_rect(center=botao_dificil.center)
    janela.blit(texto_facil, facil_rect)
    janela.blit(texto_medio, medio_rect)
    janela.blit(texto_dificil, dificil_rect)

    # botão de retorno
    janela.blit(return_symbol, botao_return)
    
    # titulo
    text = title_font.render("UNEQUAL MAZE THE CHALLENGE", True, (112, 129, 145))
    janela.blit(text, (150, 100))
    
    pygame.display.flip()

def draw_game(maze:Maze, game_mode:str, direction=None) -> Maze | None: #desenhar a tela de jogo
    janela.blit(pygame_background, (0,0)) # mete o background
    
    # dimensões do espaço do maze
    cell_size = 600// max(maze.lines, maze.columns)
    tela_size = (cell_size * maze.columns, cell_size * maze.lines)
    tela = pygame.Surface(tela_size) #tela onde vai estar o labirinto
    
    relogio = pygame.time.Clock()
    relogio.tick(20)
    
    janela.blit(return_symbol, botao_return) # botão de return
    
    if game_mode == 'player':
        
        janela.blit(retry_symbol, botao_retry) #botao de retry
        janela.blit(hint_symbol, botao_hint) #botao de hint
        maze = player_move(tela, maze, cell_size, direction) # função para desenhar o maze em si
        pygame.display.flip()
        return maze # para podermos controlar o maze atual
        
    elif game_mode == 'ia':
        draw_steps(tela, maze, cell_size) # desenha os passos 1 a 1
        pygame.display.flip()
        return
    
def draw_maze(tela,  maze, cell_size) -> None: # desenha o maze e o maze que se passa é uma np.array
    player = pygame.transform.scale(pygame_player, (cell_size//2, cell_size//2))
    end = pygame.transform.scale(pygame_end, (cell_size//2, cell_size//2))
    barrier = pygame.transform.scale(pygame_barrier, (cell_size//2, cell_size//2))
    items = {objetivo: end, cur: player, obstaculo: barrier} # dicionario para correspondencia simbolo do tabuleiro e imagem
    
    lines, columns = maze.shape
    for line in range(lines):
        for col in range(columns):
            # posicionamento de cada cell
            x, y = col * cell_size , line * cell_size
            cell = pygame.Rect( x, y, cell_size, cell_size) # pos_x, pos_y, comprimento, altura
            pygame.draw.rect(tela, (0,0,0), cell, 1) # superficie, cor, item, expessura

            cor = COR_FUNDO
            atual = maze[line, col]   

            if atual == obstaculo: 
                cor = COR_OBSTACULO
                tela.blit(items.get(obstaculo), (x + cell_size//4, y + cell_size//4))

            elif atual == objetivo: 
                cor = COR_OBJETIVO
                tela.blit(items.get(objetivo), (x + cell_size//4, y + cell_size//4))

            elif atual == cur: 
                cor = COR_POSITION
                pygame.draw.rect(tela, (0, 0, 0), cell)
                tela.blit(items.get(cur), (x + cell_size//4, y + cell_size//4))
                
            elif atual == up_symbol:
                cor = COR_ATUAL
                seta(tela, cell_size, line, col, 0)

            elif atual == down_symbol:
                cor = COR_ATUAL
                seta(tela, cell_size, line, col, 2)

            elif atual == left_symbol:
                cor = COR_ATUAL
                seta(tela, cell_size, line, col, 1)

            elif atual == right_symbol:  
                cor = COR_ATUAL      
                seta(tela, cell_size, line, col, 3) 

            else:  # Empty path
                cor = COR_PAREDE
                pygame.draw.circle(tela, COR_CIRCLE, (x + cell_size//2, y + cell_size//2), cell_size//8)  
                
            pygame.draw.rect(tela, cor, (x, y, cell_size, cell_size),10)
            pygame.draw.rect(tela, (0,0,0), (x, y, cell_size, cell_size),1)

    janela.blit(tela, ((janela_size[0] - tela.get_size()[0]) // 2,(janela_size[1] - tela.get_size()[1]) // 2))
    
def draw_steps(tela, maze:Maze, cell_size) -> None:
    for step in maze.move_history:
        draw_maze(tela, step, cell_size)
        pygame.display.update()
        time.sleep(0.3) # tempo de espera entre cada movimento

def pop_final_message(message) -> None:
    final_message_rect = pygame.Rect(0, 0, 500, 200)  # Define as dimensões do retângulo
    final_message_rect.center = janela.get_rect().center  # Centraliza o retângulo na tela
    final_text = title_font.render(message, True, COR_LETRA)
    pygame.draw.rect(janela, COR_BOTAO, final_message_rect, border_radius=50)
    text_rect = final_text.get_rect(center=final_message_rect.center)  # Centraliza o texto dentro do retângulo
    janela.blit(final_text, text_rect)

def player_move(tela, maze:Maze, cell_size, direction) -> Maze:
    next_mazes = possible_moves_player(maze)
    next_maze = next_mazes.get(direction)
    
    if next_maze is None: # se não for possivel naquela direçao
        draw_maze(tela, maze.maze, cell_size)
        return maze
    else: 
        draw_maze(tela, next_maze.maze, cell_size)
        return next_maze
        
'''
game_state:
    mode - estamos na tela de escolher o modo de jogo (ia ou player)
    menu - estamos na tela de menu a escolher a dificuldade
    easy_game, medium_game, hard_game - dificuldade do jogo e desenha o jogo
    playing - depois de ter desenhado o jogo 
    game_over - apenas no modo player quando nao ha mais movimentos possiveis
    finished - apenas no modo player quando se chega ao fim

game_mode:
    ia - ver a ia a resolver
    player - nos jogamos no W,A,S,D
'''        
# Mantém a janela aberta
running = True
game_state = 'mode'
draw_mode()
while running:
    pygame.display.update()
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN: #clicks
            
            if game_state == 'mode': # na tela de mode
                if botao_player.collidepoint(event.pos): #player button
                    game_state = 'menu'
                    game_mode = 'player'
                    draw_menu()
                elif botao_ia.collidepoint(event.pos): #ia button
                    game_state = 'menu'
                    game_mode = 'ia'
                    draw_menu()
                    
            elif game_state == 'menu': # na tela de menu
                
                if botao_facil.collidepoint(event.pos): #easy
                    initial_maze = random.choice(easy_mazes) #guarda se para se quiser repetir o jogo
                    maze = initial_maze.copy() #para nao mudar o inicial
                    final_maze = weighted_a_star_search(maze, distancia_manhattan, 2.5) #para ter a funçao de game over #para ter a funçao de game over
                    
                    if game_mode == 'ia':
                        draw_game(final_maze, game_mode) #desenha os passos
                    else:
                        draw_game(maze, game_mode) #desenha o jogo
                        
                    game_state = 'playing'
                elif botao_medio.collidepoint(event.pos): #medium
                    
                    initial_maze = random.choice(medium_mazes) #guarda se para se quiser repetir o jogo
                    maze = initial_maze.copy() #para nao mudar o inicial
                    final_maze = weighted_a_star_search(maze, distancia_manhattan, 2.5) #para ter a funçao de game over
                    
                    if game_mode == 'ia':
                        draw_game(final_maze, game_mode) #desenha os passos
                    else:
                        draw_game(maze, game_mode) #desenha o jogo
                        
                    game_state = 'playing'
                elif botao_dificil.collidepoint(event.pos): #hard
                    
                    initial_maze = random.choice(hard_mazes) #guarda se para se quiser repetir o jogo
                    maze = initial_maze.copy() #para nao mudar o inicial
                    final_maze = weighted_a_star_search(maze, distancia_manhattan, 2.5) #para ter a funçao de game over #para ter a funçao de game over
                    
                    if game_mode == 'ia':
                        draw_game(final_maze, game_mode) #desenha os passos
                    else:
                        draw_game(maze, game_mode) #desenha o jogo
                        
                    game_state = 'playing'
                elif botao_return.collidepoint(event.pos): #return
                    game_state = 'mode'
                    draw_mode()
                    
            elif game_state in {'playing', 'game_over', 'finished'}: # na tela de jogo
                if botao_return.collidepoint(event.pos):
                    game_state = 'menu'
                    draw_menu()
                
                if game_mode == 'player': # na tela de jogo com player 
                    if botao_retry.collidepoint(event.pos): #retry
                        maze = initial_maze.copy()
                        draw_game(maze, game_mode)
                        game_state = 'playing'
                        
                    if game_state == 'playing': # durante o jogo com player
                        if botao_hint.collidepoint(event.pos): # dica
                            hint = get_hint(maze, final_maze)
                            time.sleep(0.1)
                            maze = draw_game(maze, game_mode, hint)
                            if maze.is_solved():
                                time.sleep(1)
                                pop_final_message('YOU WON')
                                game_state = 'finished'
                    
        elif event.type == pygame.KEYDOWN: # tecla
            if game_mode == 'player' and game_state == 'playing': # durante o jogo com player
                if event.key == pygame.K_w: #up
                    maze = draw_game(maze, game_mode, 'up')
                elif event.key == pygame.K_s: #down
                    maze = draw_game(maze, game_mode, 'down')
                elif event.key == pygame.K_a: #left
                    maze = draw_game(maze, game_mode, 'left')
                elif event.key == pygame.K_d: #right
                    maze = draw_game(maze, game_mode, 'right')
                
                if maze.is_solved(): #jogo acabado
                    time.sleep(0.5)
                    pop_final_message('YOU WON')
                    game_state = 'finished'
                elif game_over(maze, final_maze): #game over
                    time.sleep(0.5)
                    pop_final_message('GAME OVER')
                    game_state = 'game_over'
                