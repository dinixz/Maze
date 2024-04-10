import pygame

# Inicializar Pygame
pygame.init()
# Tamanho da tela
tamanho_tela = (400, 300)


superficie = pygame.Surface((120, 120))
tamanho_celulaX, tamanho_celulay  = 40, 40 


for linha in range(3):
        for coluna in range(3):
            rec = pygame.Rect( coluna * tamanho_celulaX, linha * tamanho_celulay, tamanho_celulaX, tamanho_celulay)
            pygame.draw.rect(superficie, (255,55,5),rec,1)


# Criar a tela
tela = pygame.display.set_mode(tamanho_tela)
# Carregar imagem de fundo
imagem_fundo = pygame.image.load("game.png")

# Desenhar a imagem de fundo
tela.blit(imagem_fundo, (0, 0))

# Definir fonte e cor do texto
fonte = pygame.font.SysFont("Arial", 30)
cor_texto = (255, 255, 255)  # Branco

# Criar superfície para o texto
texto_titulo = fonte.render("Título da Tela Inicial", True, cor_texto)

# Desenhar o texto na tela
tela.blit(texto_titulo, (100, 100))
# Definir cores dos botões
cor_normal = (200, 200, 200)
cor_selecionado = (100, 100, 100)

# Criar superfície para o botão
botao_iniciar = pygame.Rect(100, 200, 100, 50)

# Desenhar o botão na tela
pygame.draw.rect(tela, cor_normal, botao_iniciar)

# Criar texto para o botão
texto_botao = fonte.render("Iniciar", True, cor_texto)

# Desenhar o texto do botão na tela
tela.blit(texto_botao, (botao_iniciar.x + 20, botao_iniciar.y + 15))
# Atualizar a tela
pygame.display.flip()

# Loop para manusear eventos
running = True
while running:
  pygame.display.flip()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    # Verificar se o mouse está sobre o botão
    if event.type == pygame.MOUSEMOTION:
      if botao_iniciar.collidepoint(event.pos):
        pygame.draw.rect(tela, cor_selecionado, botao_iniciar)
      else:
        pygame.draw.rect(tela, cor_normal, botao_iniciar)

    # Verificar se o botão foi clicado
    if event.type == pygame.MOUSEBUTTONDOWN:
      if botao_iniciar.collidepoint(event.pos):
        tela.blit(superficie, (50, 50))
        ...

# Sair do Pygame
pygame.quit()

#print(pygame.font.get_fonts())