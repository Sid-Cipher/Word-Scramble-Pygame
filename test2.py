# Importing necessary libraries
import pygame
import random
import time

# Initializing pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Scramble Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font_large = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 36)

# Game clock
clock = pygame.time.Clock()
FPS = 30

# Word bank and levels
word_bank = {
    1: ["cat", "dog", "bat", "rat", "hat"],
    2: ["apple", "grape", "peach", "mango", "berry"],
    3: ["python", "gaming", "jumble", "widget", "planet"]
}

# Global variables
current_level = 1
scrambled_word = ""
original_word = ""
user_input = ""
start_time = 0
timer_limit = 20


def scramble_word(word):
    """Scrambles the letters of a word."""
    word = list(word)
    random.shuffle(word)
    return ''.join(word)


def display_text(text, font, color, x, y, center=True):
    """Displays text on the screen."""
    render = font.render(text, True, color)
    rect = render.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(render, rect)


def get_new_word(level):
    """Fetches a new word and scrambles it."""
    global scrambled_word, original_word, start_time
    original_word = random.choice(word_bank[level])
    scrambled_word = scramble_word(original_word)
    start_time = time.time()


# Initialize the first word
get_new_word(current_level)

# Main game loop
running = True
while running:
    screen.fill(WHITE)
    elapsed_time = time.time() - start_time
    remaining_time = max(0, int(timer_limit - elapsed_time))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            elif event.key == pygame.K_RETURN:
                if user_input.lower() == original_word:
                    user_input = ""
                    current_level += 1 if current_level < len(word_bank) else 0
                    get_new_word(current_level)
                else:
                    user_input = ""
            else:
                user_input += event.unicode

    # Check if time is up
    if remaining_time == 0:
        display_text("Time's up! Game Over!", font_large, RED, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False
        continue

    # Display scrambled word, user input, level, and timer
    display_text(f"Level: {current_level}", font_small, BLACK, 10, 10, center=False)
    display_text(f"Time Left: {remaining_time}s", font_small, BLACK, WIDTH - 150, 10, center=False)
    display_text(scrambled_word, font_large, BLACK, WIDTH // 2, HEIGHT // 3)
    display_text(user_input, font_large, GREEN, WIDTH // 2, HEIGHT // 2)

    # Update the screen
    pygame.display.flip()
    clock.tick(FPS)

# Quit pygame
pygame.quit()
