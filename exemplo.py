import pygame
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Process

# Define a function to create the Pygame window
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

# Define a function to create the Matplotlib plot
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
