import pygame, sys, random
from algorithms import *

COR_PAREDE = (34, 139, 34) # green color
COR_CIRCLE = (34, 139, 34)
COR_CAMINHO = (200, 200, 200)  # Light gray for empty path
COR_FUNDO = (0, 0, 0)  # Black background
COR_OBSTACULO = (50, 50, 50)  # Dark gray for obstacles
COR_ATUAL = (200, 50, 50)  # Green for current player position
COR_OBJETIVO = (0, 0, 255)  # Blue for goal position
COR_POSITION = (255, 255, 10) 
COR_BOTAO = (255, 255, 90) #AMARELO
COR_LETRA = (50, 50, 50) # CINZA
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

pygame.init()

pygame_player = pygame.image.load('images/pacman.png')
pygame_end = pygame.image.load('images/end.png')
pygame_barrier = pygame.image.load('images/barrier.png')
pygame_return = pygame.image.load('images/return.png')
pygame_background = pygame.image.load('images/geometric.jpg')

return_symbol = pygame.transform.scale(pygame_return, (50,50))

#janela toda
janela_size = (1000, 700) 
janela = pygame.display.set_mode(janela_size)

#botões
botao_facil = pygame.Rect(400 , 300 , 150, 55)
botao_medio = pygame.Rect(400, 375, 150, 55)
botao_dificil = pygame.Rect(400, 450, 150, 55)
botao_return = return_symbol.get_rect() #cria um retangulo para conter a imagem
botao_return.center = (25,25) #posiçao na janela

def seta(tela, cell_size, linha, coluna, num): #0-up 1-left 2-down 3-right
    superficie = pygame.Surface((cell_size, cell_size)) #cria lugar da seta
    
    pygame.draw.polygon(superficie, (255, 0, 0), [[cell_size//2.1, cell_size//4], [cell_size//3.4, cell_size//2],[cell_size//1.5, cell_size//2]]) #triangulo da seta
    pygame.draw.rect(superficie, (255, 0, 0), (cell_size//2.54 , cell_size//2.5, cell_size//5, cell_size //2.7)) #retangulo da seta
    angulo_rotacao = 90  #rotaçao da seta
    superficie_rotacionada = pygame.transform.rotate(superficie, angulo_rotacao*num) #roda a celula

    tela.blit(superficie_rotacionada,( cell_size*coluna, cell_size*linha)) #desenha a seta

def draw_menu():
    janela.blit(pygame_background, (0,0))

    button_font = pygame.font.SysFont("Arial", 30)
    texto_facil = button_font.render("FÁCIL", True, COR_LETRA)
    texto_medio = button_font.render("MÉDIO", True, COR_LETRA)
    texto_dificil = button_font.render("DIFÍCIL", True, COR_LETRA)

    pygame.draw.rect(janela, COR_BOTAO, botao_facil, border_radius=10)
    pygame.draw.rect(janela, COR_BOTAO, botao_medio, border_radius=10)
    pygame.draw.rect(janela, COR_BOTAO, botao_dificil, border_radius=10)

    janela.blit(texto_facil, (botao_facil.x + 30, botao_facil.y + 10))
    janela.blit(texto_medio, (botao_medio.x +30, botao_medio.y+ 10))
    janela.blit(texto_dificil, (botao_dificil.x + 30, botao_dificil.y + 10))
    
    title_font = pygame.font.Font('freesansbold.ttf' ,40)
    text = title_font.render("UNEQUAL MAZE THE CHALLENGE", True, (112, 129, 145))
    janela.blit(text, (150, 100))
    
    pygame.display.flip()

def draw_game(maze:Maze):
    janela.blit(pygame_background, (0,0))
    
    cell_size = 600// max(maze.lines, maze.columns)
    tela_size = (cell_size * maze.columns, cell_size * maze.lines)
    tela = pygame.Surface(tela_size) #tela onde vai estar o labirinto
    
    relogio = pygame.time.Clock()
    relogio.tick(20)
    
    player = pygame.transform.scale(pygame_player, (cell_size//2, cell_size//2))
    end = pygame.transform.scale(pygame_end, (cell_size//2, cell_size//2))
    barrier = pygame.transform.scale(pygame_barrier, (cell_size//2, cell_size//2))
    
    janela.blit(return_symbol, botao_return)
    
    items = {objetivo: end, cur: player, obstaculo: barrier}
    
    draw_steps(tela, maze, cell_size, items)
    
    pygame.display.flip()

def draw_maze(tela,  maze:Maze, cell_size, items:dict): #maze é uma np.array
    lines, columns = maze.shape
    for line in range(lines):
        for col in range(columns):
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
    
def draw_steps(tela, maze:Maze, cell_size, items:dict):
    for step in maze.move_history:
        draw_maze(tela, step, cell_size, items)
        pygame.display.update()
        time.sleep(0.5)

# Mantém a janela aberta
running = True
game_state = 'menu'
while running:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == 'menu':
                if botao_facil.collidepoint(event.pos):
                    game_state = 'easy_game'
                elif botao_medio.collidepoint(event.pos):
                    game_state = 'medium_game'
                elif botao_dificil.collidepoint(event.pos):
                    game_state = 'hard_game'
            else:
                if botao_return.collidepoint(event.pos):
                    game_state = 'menu'
    
    if game_state == 'menu':
        draw_menu()
    elif game_state == 'easy_game':
        maze = random.choice(easy_mazes)
        maze = a_star_search(maze, distancia_manhattan)
        draw_game(maze)
        game_state = 'waiting'
    elif game_state == 'medium_game':
        maze = random.choice(medium_mazes)
        maze = a_star_search(maze, distancia_manhattan)
        draw_game(maze)
        game_state = 'waiting'
    elif game_state == 'hard_game':
        maze = random.choice(hard_mazes)
        maze = a_star_search(maze, distancia_manhattan)
        draw_game(maze)
        game_state = 'waiting'
