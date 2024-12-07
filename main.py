import pygame
import time
import random


#Initialziing the Pygame
pygame.init()

#Display Screen Width
screen = pygame.display.set_mode((1280,720))


#Title and Icon
pygame.display.set_caption("Word Scramble")
icon = pygame.image.load('crossword.png')
pygame.display.set_icon(icon)

# Load your high-res image
background = pygame.image.load("background.png")

# Scale it to fit the screen
WIDTH, HEIGHT = 1280,720 # Been placed here only for future references of width and height
scaled_background = pygame.transform.scale(background, (1280, 720))

#Loading the custom font
font_size = 40
font = pygame.font.Font("DJB Chalk It Up.ttf", font_size)

# Timer
start_time = 30  # Start with 30 seconds
time_left = start_time
clock = pygame.time.Clock()

# Score system

score = 0

# Word levels

easy_words = ["cat", "dog", "bat"]
medium_words = ["apple", "grape", "house"]
hard_words = ["elephant", "umbrella", "happiness"]
current_level = "easy"
words = {"easy": easy_words, "medium": medium_words, "hard": hard_words}
word_to_guess = random.choice(words[current_level])

#Functions to Code

#scramble code (Returns Scrambled)
def scramble_word(word):
    if len(word) <= 1:
        return word  # A single letter doesn't need scrambling.

    word_list = list(word)  # Convert the word to a list of characters.
    random.shuffle(word_list)  # Shuffle the characters randomly.

    scrambled = ''.join(word_list)  # Join the shuffled characters back into a string.

    # Ensure the scrambled word isn't the same as the original.
    while scrambled == word:
        random.shuffle(word_list)
        scrambled = ''.join(word_list)

    return scrambled

#timer_function
def display_timer(screen, font, time_left):
    """
    Draws a timer on the screen, changing color based on time remaining.

    Parameters:
    screen: Pygame screen object where the timer will be displayed.
    font: The Pygame font object for rendering the timer.
    time_left: The remaining time (in seconds).
    """
    # Change color based on time
    if time_left >= 10:
        color = (255, 255, 255)  # White
    else:
        color = (255, 0, 0)  # Red

    # Render the timer text
    timer_text = font.render(f"Time Left: {time_left}", True, color)

    # Get the text's rectangle and center it on the screen
    timer_rect = timer_text.get_rect(center=(640, 50))  # Adjust the position as needed

    # Draw the text on the screen
    screen.blit(timer_text, timer_rect)


#game Loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:




    # Draw the scaled background
    screen.blit(scaled_background, (0, 0))

    # Update the display
    pygame.display.flip()

pygame.quit()





