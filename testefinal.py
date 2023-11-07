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
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Soccer Field")


with open('ball_trajectory.txt', 'r') as file:
    linhas = file.read().splitlines()

# Variables

x_robo = float(input("Enter Coordinates X: "))
y_robo = float(input("Enter Coordinates Y: "))

user_inputx = (x_robo*100)
user_inputy = (y_robo*100)

robot_image = pygame.image.load("robofeif.png")
robot_image = pygame.transform.scale(robot_image,(20,20))


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

interception_time = temp(x_robo, y_robo)

def calculate_new_robot_position(x_robo, y_robo, interception_time):
    velocidade_robo = 2.8  # m/s

    # Assuming time increment (0.2 seconds per frame for example)
    time_increment = 0.2

    # Calculate the number of frames needed to reach the interception time
    frames = int(interception_time / time_increment)

    # Calculate the total distance covered by the robot in frames
    total_distance = velocidade_robo * frames

    # Calculate the angle between current position and ball position
    # For example, assuming the ball is at (x_ball, y_ball)
    angle = math.atan2(y_ball - y_robo, x_ball - x_robo)

    # Calculate the new position based on the total distance and angle
    new_x_robo = (x_robo + total_distance * math.cos(angle))*10
    new_y_robo = (y_robo + total_distance * math.sin(angle))*10

    return new_x_robo, new_y_robo

def draw_ball(x_ball, y_ball):
    pygame.draw.circle(screen, ball_color, (int(x_ball), int(y_ball)), 5)

def draw_robot(user_inputx, user_inputy):
    screen.blit(robot_image, (user_inputx - robot_image.get_width() // 2, user_inputy - robot_image.get_height() // 2))


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



def draw_text():
    font = pygame.font.Font(None, 360)
    text = "Hello, Pygame!"
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)


# Main loop juego

pygame.init()
clock = pygame.time.Clock()

tiempo = 0


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
        draw_ball((x_ball*100), (y_ball*100))
        index += 1  # Move to the next position in the trajectory

    if interception_time:
        # Calculate the robot's new position based on time
        new_x, new_y = calculate_new_robot_position(x_robo, y_robo, interception_time)

        newx = new_x*5
        newy = new_y

        # Draw the robot at its new position
        draw_robot(newx, newy)
    
    frames = int(interception_time / 0.2)  # Assuming each frame represents 0.2 seconds

    for frame in range(frames):
    # Calculate intermediate position based on frame
        progress = (frame + 1) / frames  # Progress from 0 to 1
        tiempo += 1
        intermediate_x = user_inputx + (newx - user_inputx) * progress
        intermediate_y = user_inputy + (newy - user_inputy) * progress
        if intermediate_x >= 10 and intermediate_y >= 6:
            draw_robot(intermediate_x, intermediate_y)
    
    

# Finally, draw the robot at the final position (new_x, new_y)
    draw_robot(user_inputx, user_inputy)
    
    draw_text()
    pygame.display.update()
    clock.tick(3)  # Set the frame rate to 60 frames per second

# Quit Pygame
pygame.quit()
sys.exit()
