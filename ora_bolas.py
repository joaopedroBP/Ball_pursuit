import pygame
import math
import threading
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Process

X0_robo = float(input("Enter the initial x position of the robot: "))
Y0_robo = float(input("Enter the initial y position of the robot: "))

#função(ões) ora_bolas!

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def temp(x_robo,y_robo):
    velocidade_robo = 2.8  # m/s
    acelercao_robo = 2.8  # m/s^2
    raio_interceptacao = 0.0943  # 9.43 em m 

    # lendo o trajetoria da bola
    with open('ball_trajectory.txt', 'r') as file:
        linhas = file.read().splitlines()

    #substituir "." por "."
    for line in linhas[1:]:  
        t, x_ball, y_ball = map(lambda val: float(val.replace(',', '.')), line.split())
    
        # Calcular a distância entre o robo e um ponto da trajetoria da bola.
        distance_to_ball = distance(x_robo, y_robo, x_ball, y_ball)
    
        # Calcular o tempo que o robo leva pra percorrer esse distância.
        robot_time = math.sqrt((2 * distance_to_ball) / acelercao_robo)
    
        if robot_time <= t:
            return t
        else:
            # Calculate the new position of the robot after t seconds
            new_x_robo = x_robo + (t / 0.2) * velocidade_robo
            new_y_robo = y_robo + (t / 0.2) * velocidade_robo
        
            # Calculate the distance between the new robot position and the ball's position at time t
            new_distance_to_ball = distance(new_x_robo, new_y_robo, x_ball, y_ball)
        
            if new_distance_to_ball <= raio_interceptacao:
                return t;

# Função do pygame!
def pygame_window():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pygame Window")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        pygame.display.flip()

    pygame.quit()

# Função dos graficos do robo!
def graficos_robo():

    # variaveis importantes
    x0 = None
    y0 = None
    Xf = None
    Yf = None
    tempoMax = None
    Tintervalos = 0.02
    num = 0
    check_time = temp(X0_robo,Y0_robo)
    # listas
    Ball_posX = []
    Ball_posY  = []
    Ball_velx = []
    Ball_vely = []
    Ball_ax = []
    Ball_ay = []
    Posrx = []
    Posry = []
    Velrx = []
    Velry = []
    Acrx  = []
    Acry =  []
    dist_to_ball = []
    curent_time = []
    check1 = []
    check2 = []


    with open('ball_trajectory.txt', 'r') as file:
        linhas = file.read().splitlines()

    #substituir "." por "."
    for line in linhas[1:]:  
        t, x_ball, y_ball = map(lambda val: float(val.replace(',', '.')), line.split())
        Ball_posX.append(x_ball)
        Ball_posY.append(y_ball)
        if t == check_time:
            x0 = X0_robo
            y0 = Y0_robo
            Xf = x_ball
            Yf = y_ball
            tempoMax = t
            curent_time.append(0)
            Ball_posX.append(x_ball)
            Ball_posY.append(y_ball)
            break

    if x0 is not None and y0 is not None and Xf is not None and Yf is not None:
        angulo = math.atan((abs(Yf - y0))/(abs(Xf - x0)))
        distMax = distance(x0, y0, Xf, Yf)
        dist_to_ball.append(0)


        Numintervalos = (tempoMax/Tintervalos)
        Velrx.append(0)
        Velry.append(0)



        for i in range (int(Numintervalos) ):
            num = num + 0.02
            check1.append(num)
            distancia  = 0 + 0 + (2.8/2) * (num ** 2)
            check2.append(distancia)
            if x0 > Xf:
                Xdistance = x0 - ((distMax - distancia) * (math.cos(angulo)))
            elif x0 <= Xf:
                Xdistance = x0 + ((distMax - distancia) * (math.cos(angulo)))
            if y0 > Yf: 
                Ydistance = y0 - ((distMax - distancia) * math.sin(angulo))
            elif y0 <= Yf:
                 Ydistance = y0 + ((distMax - distancia) * math.sin(angulo))

            Newdistance_to_ball = distance(Xdistance,Ydistance,Xf,Yf)
            dist_to_ball.append(Newdistance_to_ball)
            curent_time.append(num)

            Newvelx = Xdistance * num
            if Newvelx > 2.8:
                Newvelx = 2.8
            Newvely = Ydistance *num
            if Newvely > 2.8:
                Newvely = 2.8

            Newax = Newvelx * num
            if Newax > 2.8:
                Newax = 2.8
            elif Newax < 0:
                Newax = 0
            Neway = Newvely * num
            if Neway > 2.8:
                Neway = 2.8
            elif Neway < 0:
                Neway = 0

            Posrx.append(Xdistance)
            Posry.append(Ydistance)
            Velrx.append(Newvelx)
            Velry.append(Newvely)
            Acrx.append(Newax)
            Acry.append(Neway)
            
        Acrx.append(2.8)
        Acry.append(2.8)
        Posrx.append(x0)
        Posry.append(y0)    
        Acrx.reverse()
        Acry.reverse()
        Posrx.reverse()
        Posry.reverse()
        dist_to_ball.reverse()

    #Arquivos com informações da Bola


    with open('Vx_bola.txt','r') as file:
        linhas = file.read().splitlines()

    #substituir "." por "."
    for line in linhas[1:]:  
        t, Vx_ball= map(lambda val: float(val.replace(',', '.')), line.split())
        Ball_velx.append(Vx_ball)
        if t == check_time:
            Ball_velx.append(Vx_ball)
            break 
    
    with open('Vy_bola.txt','r') as file:
        linhas = file.read().splitlines()

    #substituir "." por "."
    for line in linhas[1:]:  
        t, Vy_ball = map(lambda val: float(val.replace(',', '.')), line.split())
        Ball_vely.append(Vy_ball)
        if t == check_time:
            Ball_vely.append(Vy_ball)
            break

    with open('Ax_bola.txt','r') as file:
        linhas = file.read().splitlines()

    #substituir "." por "."
    for line in linhas[1:]:  
        t, Ax_ball = map(lambda val: float(val.replace(',', '.')), line.split())
        Ball_ax.append(Ax_ball)
        if t == check_time:
            Ball_ax.append(Ax_ball)
            break

    with open('Ay_bola.txt','r') as file:
        linhas = file.read().splitlines()

    #substituir "." por "."
    for line in linhas[1:]:  
        t, Ay_ball = map(lambda val: float(val.replace(',', '.')), line.split())
        Ball_ay.append(Ay_ball)
        if t == check_time:
            Ball_ay.append(Ay_ball)
            break
    

    #Gráficos 

    #gráfico das trajetorias da bola e do robo até o ponto de interceptação

    plt.figure(1)
    plt.plot(Ball_posX,Ball_posY, label='trajetoria da bola', color='blue')
    plt.plot(Posrx,Posry,label='trajetoria do robo',color='red')
    plt.xlabel("Posição x (m)")
    plt.ylabel("posição y(m)")
    plt.title("Trajetorias X e Y da bola e do robo")
    plt.legend()

    #gráfico das posições x e y do robo e da bola em função do tempo

    plt.figure(2)
    plt.plot(curent_time,Ball_posX,label='Posição x da bola em função do tempo', color='blue')
    plt.plot(curent_time,Ball_posY,label='posição y da bola em função do tempo',color='green')
    plt.plot(curent_time,Posrx,label='posição x do robo em função do tempo',linestyle='--',color='red')
    plt.plot(curent_time,Posry,label='Posião y do robo em função do tempo', linestyle='--',color='black')
    plt.xlabel("Tempo(s)")
    plt.ylabel("Posição X/Y (m)")
    plt.title("Posições x e y do robo e da bola em função do tempo")
    plt.legend()

    #gráfico velocidade x/y do robo e da bola em função do tempo
    plt.figure(3)
    plt.plot(curent_time,Ball_velx, label='Velocidade X da bola', color='blue')
    plt.plot(curent_time,Ball_vely, label='Velocidade Y da bola',color='green')
    plt.plot(curent_time,Velrx,label='Velocidade X do robo',linestyle='--',color='red')
    plt.plot(curent_time,Velry,label='Velocidade Y do robo',linestyle='--',color='black')
    plt.xlabel("Tempo(s)")
    plt.ylabel("Velocidade X/Y(m/s)")
    plt.title("Velocidades X/Y do robo e da bola em função do tempo")
    plt.legend()

    #gráfico da aceleração x/y do robo e da bola em função do tempo
    plt.figure(4)
    plt.plot(curent_time,Ball_ax, label='Aceleração X da bola', color='blue')
    plt.plot(curent_time,Ball_ay, label='Aceleração Y da bola',color='green')
    plt.plot(curent_time,Acrx,label='Aceleração X do robo',linestyle='--',color='red')
    plt.plot(curent_time,Acry,label='Aceleração Y do robo',linestyle='--',color='black')
    plt.xlabel("Tempo(s)")
    plt.ylabel("Aceleração X/Y(m/s²)")
    plt.title("Aceleração X/Y do robo e da bola em função do tempó")
    plt.legend()

    #gráfico da distância relativa entre o robo e a bola
    plt.figure(5)
    plt.plot(curent_time,dist_to_ball,label='distance to ball',color='blue')
    plt.xlabel("Tempo(s)")
    plt.ylabel("Distância do robo para a bola")
    plt.title("Distância do robo para a bola em relação ao tempo")
    plt.legend()

    plt.show()
    return 0
        

pygame_thread = threading.Thread(target=pygame_window)

# Start the pygame thread
pygame_thread.start()

# Run the matplotlib code in the main thread
graficos_robo()

# Wait for the pygame thread to finish
pygame_thread.join()




