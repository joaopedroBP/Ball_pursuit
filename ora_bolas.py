import pygame
import math
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Process

#função(ões) ora_bolas!

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def temp():
    velocidade_robo = 2.8  # m/s
    acelercao_robo = 2.8  # m/s^2
    raio_interceptacao = 0.0943  # 9.43 em m 

    x_robo = float(input("Enter the initial x position of the robot: "))
    y_robo = float(input("Enter the initial y position of the robot: "))

    # lend o trajetoria da bola
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
            print(f"Robot intercepts the ball at t = {t} seconds, x = {x_ball} meters, y = {y_ball} meters.")
            return t
        else:
            # Calculate the new position of the robot after t seconds
            new_x_robo = x_robo + (t / 0.2) * velocidade_robo
            new_y_robo = y_robo + (t / 0.2) * velocidade_robo
        
            # Calculate the distance between the new robot position and the ball's position at time t
            new_distance_to_ball = distance(new_x_robo, new_y_robo, x_ball, y_ball)
        
            if new_distance_to_ball <= raio_interceptacao:
                print(f"Robot intercepts the ball at t = {t} seconds, x = {x_ball} meters, y = {y_ball} meters.")
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

# Função dos graficos!
def matplotlib_plot():
    x = np.linspace(-10, 10, 100)
    y = x**2
    plt.plot(x, y)
    plt.title("Function y = x^2")
    plt.show()

if __name__ == "__main__":
    # Create two separate processes for Pygame and Matplotlib
    pygame_process = Process(target=pygame_window)
    matplotlib_process = Process(target=matplotlib_plot)

    # Start both processes
    pygame_process.start()
    matplotlib_process.start()

    # Wait for both processes to finish
    pygame_process.join()
    matplotlib_process.join()



