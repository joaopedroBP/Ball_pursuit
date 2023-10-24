import pygame

pygame.init()

altura_tela = 500
largura_tela = 500

tela = pygame.display.set_mode((altura_tela,largura_tela))
robo = pygame.Rect((300,250,50,50))


run = True
while run:
    pygame.draw.rect(tela,(255,0,0),robo)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
