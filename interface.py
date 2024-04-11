import pygame
from Maze import * 
import sys
import math
from algorithms import depth_first_search


#CORES
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
maze = Maze(3,3)


tela_completa = (1000, 700)
tela_comp = pygame.display.set_mode(tela_completa)

#INICIAL
font = pygame.font.Font('freesansbold.ttf' ,40)
text = font.render("UNEQUAL MAZE THE CHALLENGE", True, (255, 0, 0))
tela_comp.blit(text, (100, 100))


#JOGO
tamanho_celula = 600// max(maze.lines, maze.columns)# Adjust cell size based on window size

wit, heig = tamanho_celula * maze.columns, tamanho_celula *maze.lines
tamanho_tela = (wit, heig)
tela = pygame.Surface(tamanho_tela)


relogio = pygame.time.Clock()

def seta(tela, linha, coluna, num):
    superficie = pygame.Surface((tamanho_celula, tamanho_celula))
    pygame.draw.polygon(superficie, (255, 0, 0), [[tamanho_celula//2.1,tamanho_celula//4], [tamanho_celula//3.4,tamanho_celula//2],[tamanho_celula//1.5, tamanho_celula//2]])
    pygame.draw.rect(superficie, (255, 0, 0), (tamanho_celula//2.54 , tamanho_celula//2.5, tamanho_celula//5,  tamanho_celula //2.7))
    angulo_rotacao = 90  # Ângulo de rotação em graus
    superficie_rotacionada = pygame.transform.rotate(superficie, angulo_rotacao*num)

    tela.blit(superficie_rotacionada,( tamanho_celula*coluna, tamanho_celula*linha))

pygame_image = pygame.image.load('pacman.png')
pygame_end = pygame.image.load('end.png')
pygame_barrier = pygame.image.load('barrier.png')

player = pygame.transform.scale(pygame_image, (tamanho_celula//2, tamanho_celula//2))
end = pygame.transform.scale(pygame_end, (tamanho_celula//2, tamanho_celula//2))
barrier = pygame.transform.scale(pygame_barrier, (tamanho_celula//2, tamanho_celula//2))

def desenhar_labirinto(maze):
    tela_comp.blit(caixaDeTexto(ficie, "hints",(50, 20), 20), (770, 200))

    for linha in range(maze.lines):
        for coluna in range(maze.columns):
            x, y = coluna * tamanho_celula , linha * tamanho_celula
            rec = pygame.Rect( x, y, tamanho_celula, tamanho_celula)
            pygame.draw.rect(tela, (0,0,0),rec,1)

            cor = COR_FUNDO
            atual = maze.maze[linha][coluna]   
            rec = pygame.Rect(x, y, tamanho_celula, tamanho_celula)

            if atual == "#":  # Obstacle
                cor = COR_OBSTACULO
                tela.blit(barrier, (x + tamanho_celula//4, y + tamanho_celula//4))

            elif atual == "\x1b[34mO\x1b[0m":  # Goal position
                cor = COR_OBJETIVO
                tela.blit(end, (x + tamanho_celula//4, y + tamanho_celula//4))

            elif atual == "\x1b[32mX\x1b[0m": # actual position
                cor = COR_POSITION
                pygame.draw.rect(tela, (0, 0, 0), rec)
                tela.blit(player, (x + tamanho_celula//4, y + tamanho_celula//4))
                
            elif atual == "↑":
                cor = COR_ATUAL
                seta(tela, linha, coluna, 0)

            elif atual == "↓":
                cor = COR_ATUAL
                seta(tela, linha, coluna, 2)

            elif atual == '←':
                cor = COR_ATUAL
                seta(tela, linha, coluna, 1)

            elif atual == "→":  
                cor = COR_ATUAL      
                seta(tela, linha, coluna, 3) 

            else:  # Empty path
                cor = COR_PAREDE
                pygame.draw.circle(tela, COR_CIRCLE, (x + tamanho_celula//2, y + tamanho_celula//2), tamanho_celula//8)  # Draw white border with width 2
            pygame.draw.rect(tela, cor, (x, y, tamanho_celula, tamanho_celula),10)
            pygame.draw.rect(tela, (0,0,0), (x, y, tamanho_celula, tamanho_celula),1)

    tela_comp.blit(tela, ((tela_completa[0] - wit) // 3,(tela_completa[1] - heig) // 3))

ficie = pygame.Surface((150, 55))



def caixaDeTexto(superficie, texto, posi, tamanhoLetra = 20, fonte = 'freesansbold.ttf',  corCaixa = (255, 255, 90) , corLetra = (50, 50, 50) ):
    pygame.draw.rect(superficie, corCaixa, (0,0, 150, 55),30,  border_radius=10)
    font = pygame.font.Font(fonte ,tamanhoLetra)
    text = font.render(texto, True, corLetra)
    superficie.blit(text, posi)
    return superficie

tela_comp.blit(caixaDeTexto(ficie, "hints",(50, 20), 20), (770, 200))


# Tela inicial
# pygame_menu = pygame.image.load('geometric.jpg')

# tam_inicial = (1000, 700)
# tela_inicial = pygame.Surface(tam_inicial)
# tela_inicial.blit(pygame_menu, (0,0))

# fonte = pygame.font.SysFont("Arial", 30)
# texto_facil = fonte.render("FÁCIL", True, COR_LETRA)
# texto_medio = fonte.render("MÉDIO", True, COR_LETRA)
# texto_dificil = fonte.render("DIFÍCIL", True, COR_LETRA)

# botao_facil = pygame.Rect(400 , 300 , 150, 55)
# botao_medio = pygame.Rect(400, 375, 150, 55)
# botao_dificil = pygame.Rect(400, 450, 150, 55)

# pygame.draw.rect(tela_inicial, COR_BOTAO, botao_facil,border_radius=10)
# pygame.draw.rect(tela_inicial, COR_BOTAO, botao_medio,border_radius=10)
# pygame.draw.rect(tela_inicial, COR_BOTAO, botao_dificil,border_radius=10)

# tela_inicial.blit(texto_facil, (botao_facil.x + 40, botao_facil.y + 10))
# tela_inicial.blit(texto_medio, (botao_medio.x +30, botao_medio.y+ 10))
# tela_inicial.blit(texto_dificil, (botao_dificil.x + 30, botao_dificil.y + 10))


# font = pygame.font.Font('freesansbold.ttf' ,40)
# text = font.render("UNEQUAL MAZE THE CHALLENGE", True, (112, 129, 145))
# tela_inicial.blit(text, (150, 100))


# tela_comp.blit(tela_inicial,(0,0))



# Tela inicial
pygame_menu = pygame.image.load('geometric.jpg')


tam_inicial = (1000, 700)
tela_inicial = pygame.Surface(tam_inicial)
tela_inicial.blit(pygame_menu, (0,0))

fonte = pygame.font.SysFont("Arial", 30)
texto_facil = fonte.render("FÁCIL", True, COR_LETRA)
texto_medio = fonte.render("MÉDIO", True, COR_LETRA)
texto_dificil = fonte.render("DIFÍCIL", True, COR_LETRA)

offset_x = (tela_comp.get_width() - tela_inicial.get_width()) // 2
offset_y = (tela_comp.get_height() - tela_inicial.get_height()) // 2


botao_facil = pygame.Rect(400 , 300 , 150, 55)
botao_medio = pygame.Rect(400, 375, 150, 55)
botao_dificil = pygame.Rect(400, 450, 150, 55)

pygame.draw.rect(tela_inicial, COR_BOTAO, botao_facil,border_radius=10)
pygame.draw.rect(tela_inicial, COR_BOTAO, botao_medio,border_radius=10)
pygame.draw.rect(tela_inicial, COR_BOTAO, botao_dificil,border_radius=10)

tela_inicial.blit(texto_facil, (botao_facil.x + 40, botao_facil.y + 10))
tela_inicial.blit(texto_medio, (botao_medio.x +30, botao_medio.y+ 10))
tela_inicial.blit(texto_dificil, (botao_dificil.x + 30, botao_dificil.y + 10))


font = pygame.font.Font('freesansbold.ttf' ,40)
text = font.render("UNEQUAL MAZE THE CHALLENGE", True, (112, 129, 145))
tela_inicial.blit(text, (150, 100))


tela_comp.blit(tela_inicial,(0,0))


running = True
while running:
    # Limpar a tela
    pygame.display.update()

    # Atualizar a tela

    # Limitar a taxa de quadros
    relogio.tick(60)

    # Tratar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if botao_facil.collidepoint(evento.pos):
                tela_inicial.fill(COR_FUNDO)
                maze = depth_first_search(maze)
        
                desenhar_labirinto(maze)


            elif botao_medio.collidepoint(evento.pos):
                
                desenhar_labirinto(maze)
            elif botao_dificil.collidepoint(evento.pos):
                desenhar_labirinto(maze)


pygame.quit()
       