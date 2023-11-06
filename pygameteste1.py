import pygame
import math
import numpy as np
from multiprocessing import Process
import sys

# Constantes

WIDTH, HEIGHT = 900, 600
FIELD_COLOR = (0, 128, 0)  # Green color for the field
LINE_COLOR = (255, 255, 255)  # White color for lines
ball_color = (255, 0, 0)
RECT_COLOR = (0, 0, 128)
Green = (0,255,0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Soccer Field")


with open('ball_trajectory.txt', 'r') as file:
    linhas = file.read().splitlines()

# Variables

userx = int(input("Enter Coordinates X: "))
usery = int(input("Enter Coordinates Y: "))

user_inputx = (userx*20)
user_inputy = (usery*20)



# Funções

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def temp(x_robo,y_robo):
    velocidade_robo = 2.8  # m/s
    acelercao_robo = 2.8  # m/s^2
    raio_interceptacao = 0.0943  # 9.43 em m 

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
                return t


def draw_ball(x_ball, y_ball):
    pygame.draw.circle(screen, ball_color, (int(x_ball), int(y_ball)), 5)

def draw_robot(user_inputx, user_inputy):
    pygame.draw.circle(screen, RECT_COLOR, (user_inputx, user_inputy), 9)


def draw_field():
    # Fill the background with the field color
    screen.fill(FIELD_COLOR)

    # Draw the boundaries
    pygame.draw.rect(screen, LINE_COLOR, (50, 50, WIDTH - 100, HEIGHT - 100), 5)

    # Draw the center line
    pygame.draw.line(screen, LINE_COLOR, (WIDTH // 2, 50), (WIDTH // 2, HEIGHT - 50), 5)

    # Draw the center circle
    pygame.draw.circle(screen, LINE_COLOR, (WIDTH // 2, HEIGHT // 2), 75, 5)

    # Draw the goal areas
    pygame.draw.rect(screen, LINE_COLOR, (50, HEIGHT // 4, 100, HEIGHT // 2), 5)
    pygame.draw.rect(screen, LINE_COLOR, (WIDTH - 150, HEIGHT // 4, 100, HEIGHT // 2), 5)




# Main loop juego

pygame.init()
clock = pygame.time.Clock()


running = True
index = 0  # Track the index in the ball trajectory data
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the display
    screen.fill(FIELD_COLOR)
    draw_field()

    for line in linhas[1:]:  
        t, x_ball, y_ball = map(lambda val: float(val.replace(',', '.')), line.split())
        draw_ball((x_ball*20), (y_ball*20))
        index += 1  # Move to the next position in the trajectory

    draw_robot(user_inputx, user_inputy)
    

    pygame.display.update()
    clock.tick(60)  # Set the frame rate to 60 frames per second

# Quit Pygame
pygame.quit()
sys.exit()
