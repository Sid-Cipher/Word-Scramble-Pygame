import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Word Scrambling Game")
font = pygame.font.Font(None, 48)

# List of words
words = ["python", "keyboard", "monitor", "coding", "pygame"]

def scramble_word(word):
    word_letters = list(word)
    random.shuffle(word_letters)
    return ''.join(word_letters)

def display_message(text, color, y_offset=0):
    message = font.render(text, True, color)
    text_rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(message, text_rect)

def game_loop():
    running = True
    word_to_guess = random.choice(words)
    scrambled_word = scramble_word(word_to_guess)
    user_guess = ""
    hint_given = False

    while running:
        screen.fill(BLACK)

        # Display the scrambled word
        display_message(f"Scrambled: {scrambled_word}", WHITE, -50)

        # Display the hint if given
        if hint_given:
            display_message(f"Hint: Starts with '{word_to_guess[0]}'", GREEN, 50)

        # Display the user's current guess
        display_message(f"Your Guess: {user_guess}", WHITE, 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_guess.lower() == word_to_guess.lower():
                        display_message("Correct! Press R to restart or Q to quit.", GREEN)
                        pygame.display.update()
                        pygame.time.wait(2000)
                        return  # Exit the loop to restart or quit
                    else:
                        display_message("Wrong! Try again.", RED)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        user_guess = ""  # Reset the guess
                elif event.key == pygame.K_BACKSPACE:
                    user_guess = user_guess[:-1]
                elif event.key == pygame.K_h:  # Press 'H' for hint
                    hint_given = True
                elif event.key == pygame.K_r:  # Press 'R' to restart
                    game_loop()  # Restart the game
                elif event.key == pygame.K_q:  # Press 'Q' to quit
                    running = False
                else:
                    user_guess += event.unicode

        pygame.display.update()

# Start the game
game_loop()
pygame.quit()
