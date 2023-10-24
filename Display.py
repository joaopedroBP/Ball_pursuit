import pygame
from ora_bolas import *
pygame.init()

altura_tela = 500
largura_tela = 500



# posição inicial do robo
x_robo = float(input("Enter the initial x position of the robot: "))
y_robo = float(input("Enter the initial y position of the robot: "))

robo = pygame.Rect((x_robo,y_robo,50,50))

tempo = temp(x_robo,y_robo)

if(tempo == None):
    print("As cordenadas iniciais do robo tornam impossível a interceptação!")

else:
    tela = pygame.display.set_mode((altura_tela,largura_tela))
    run = True
    while run:
        pygame.draw.rect(tela,(255,0,0),robo)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
