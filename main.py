import pygame
import time
import random

from matplotlib.pyplot import pause

#Initialziing the Pygame
pygame.init()

#Display Screen Width
screen = pygame.display.set_mode((1280,720))


#Title and Icon
pygame.display.set_caption("Word Scramble")
icon = pygame.image.load('crossword.png')
pygame.display.set_icon(icon)

#Loading the Assets 😭
hint_button = pygame.image.load("hint_button.png")
hint_button = pygame.transform.scale(hint_button, (110, 132))
pause_button = pygame.image.load("pause_button.png")
pause_button = pygame.transform.scale(pause_button, (62, 70))

# Load your high-res image
background = pygame.image.load("background.png")

# Scale it to fit the screen
WIDTH, HEIGHT = 1280,720 # Been placed here only for future references of width and height
scaled_background = pygame.transform.scale(background, (1280, 720))

#Loading the custom font (#Been here for future references
font_size = 40
font = pygame.font.Font("DJB Chalk It Up.ttf", font_size)

# Timer
start_time = 30  # Start with 30 seconds
time_left = start_time
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()  # Record the starting tick (in milliseconds)

# Score system

score = 1647

# Word levels

easy_words = ["cat", "dog", "bat"]
medium_words = ["apple", "grape", "house"]
hard_words = ["elephant", "umbrella", "happiness"]
current_level = "easy"
words = {"easy": easy_words, "medium": medium_words, "hard": hard_words}
word_to_guess = random.choice(words[current_level])
user_input = ""

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

def pause(screen):

    # Drawing the pause button on screen

    pass

def hint(screen):
    pass
    # Drawing the hint button on screen

def score(screen, font):

    # Drawing the score button on screen

    font_size = 70
    font = pygame.font.Font("DJB Chalk It Up.ttf", font_size)

    #Score function yet to be created !!
    pass

#timer_function
def display_timer(screen, font, time_left, elapsed_time):

   #Drawing a timer on the screen

    font_size = 98
    font = pygame.font.Font("DJB Chalk It Up.ttf", font_size)

    time_left = max(0, start_time - elapsed_time)  # Ensure it doesn't go negative

    # Change color based on time
    if time_left > 10:
        color = (255, 255, 255)  # White
    else:
        color = (255, 0, 0)  # Red

    # Render the timer text
    timer_text = font.render(f"{int(time_left)}", True, color)

    # Get the text's rectangle and center it on the screen
    timer_rect = timer_text.get_rect(center=(1137, 40))  # Adjust position as needed

    # Draw the text on the screen
    screen.blit(timer_text, timer_rect)

    return time_left


#game Loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Capture user input through the keyboard
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Check if the user presses Enter
                # Check if the guessed word is correct
                if user_input.lower() == word_to_guess.lower():
                    print("Correct!")
                    # Update score or level
                    score += 1
                    # Select a new word and scramble it
                    word_to_guess = random.choice(words[current_level])
                    scrambled_word = scramble_word(word_to_guess)
                    user_input = ""  # Reset input for the next word
                else:
                    print("Try Again!")
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]  # Remove the last character
            else:
                user_input += event.unicode  # Add the typed character to user input

    #Draw the hint button and pause button
    screen.blit(hint_button, (28, 578))
    screen.blit(pause_button, (1161,609))

    # Draw the scrambled word on the screen
    scrambled_text = font.render(f"Scrambled: {scramble_word}", True, (255, 255, 255))
    screen.blit(scrambled_text, (100, 200))  # Adjust position as needed

    # Draw user input on the screen
    user_input_text = font.render(f"Your Guess: {user_input}", True, (255, 255, 255))
    screen.blit(user_input_text, (100, 300))  # Adjust position as needed

    # Calculate elapsed time
    current_ticks = pygame.time.get_ticks()
    elapsed_time = (current_ticks - start_ticks) / 1000  # Convert milliseconds to seconds

    # Clear the screen and draw the background
    screen.blit(scaled_background, (0, 0))

    # Call the timer function
    time_left = display_timer(screen, font, start_time, elapsed_time)

    # End the game when the timer reaches zero
    if time_left <= 0:
        running = False
        print("Time's up!")  #prints in console

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)  # 30 FPS




    # Draw the scaled background
    screen.blit(scaled_background, (0, 0))

    # Update the display
    pygame.display.flip()

pygame.quit()





