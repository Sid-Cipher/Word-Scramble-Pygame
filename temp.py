import pygame
import random

# Initialize Pygame
pygame.init()

# Game Window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Number Match")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Game Variables
score = 0
time_left = 120  # 2 minutes
level = 1
max_score = 0

# Function to generate the number grid
def generate_grid(grid_size):
    grid = []
    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            row.append(random.randint(1, 9))
        grid.append(row)
    return grid

# ... other functions for checking pairs, removing pairs, adding numbers, displaying scores, etc.

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if a number was clicked and handle the click
            # ...

    # Update game state (time, score, level, etc.)
    # ...

    # Render the game elements (grid, numbers, score, time, etc.)
    screen.fill(white)
    # ... draw the grid, numbers, and text
    pygame.display.update()

pygame.quit()