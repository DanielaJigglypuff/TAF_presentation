import math
import numpy as np
import pygame
from pygame.locals import *

import RacingLineGame as RLG
import Spline

# Algorithmically generating a racing line is quite tricky. This simple framework
# allows me to explore different methods. Use mouse to drag points, and A & S keys
# to change the number of iterations.

# See Programming Splines! Videos
# Initialize the Pygame library
pygame.init()

width, height = 800, 600  # Set the desired window size

# Create the Pygame screen object with the specified width and height
screen = pygame.display.set_mode((width, height))

# Create a Pygame clock object for controlling the frame rate
clock = pygame.time.Clock()

# Create an instance of the RacingLineGame class
game = RLG.RacingLineGame()

# Initialize the game console with the specified width, height, font width, and font height
game.ConstructConsole(width, height, 2, 2)  # Adjust the font width and height as needed

# Call the OnUserCreate() method of the game object to initialize the game state
game.OnUserCreate()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    # Get the elapsed time since the last frame and limit the frame rate to 60 FPS
    fElapsedTime = clock.tick(60) / 1000.0

    # Call the OnUserUpdate() method of the game object to update the game state
    game.OnUserUpdate(fElapsedTime)

    # Set the caption of the game window to display the current FPS
    pygame.display.set_caption("Racing Line Game - FPS: " + str(int(clock.get_fps())))

    # Update the game display
    pygame.display.flip()

