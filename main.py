import pygame
import time
import random
import winsound

#Initialziing the Pygame
pygame.init()

#Display Screen Width
screen = pygame.display.set_mode((1280,720))

#Title and Icon
pygame.display.set_caption("Word Scramble")
icon = pygame.image.load('crossword.png')
pygame.display.set_icon(icon)

#Loading the Assets 😭 (crying in pressure)
hint_button = pygame.image.load("hint_button.png")
hint_button = pygame.transform.scale(hint_button, (110, 132))
pause_button = pygame.image.load("pause_button.png")
pause_button = pygame.transform.scale(pause_button, (62, 70))
pause_menu = pygame.image.load("Pause_menu.png")
pause_menu = pygame.transform.scale(pause_menu,(1280,720))

#Loading the background
background = pygame.image.load("background.png")
WIDTH, HEIGHT = 1280,720 # Been placed here only for future references of width and height
scaled_background = pygame.transform.scale(background, (1280, 720))

#Loading the custom font (#Been here for future references) (Delete during final product demo)
font_size = 40
try:
    font = pygame.font.Font("DJB Chalk It Up.ttf", font_size)
except FileNotFoundError:
    font = pygame.font.SysFont(None, font_size)

# Timer 🕛
start_time = 30  # Start with 30 seconds
time_left = start_time
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()  # Record the starting tick (in milliseconds)

# Score system
score = 1647

# Words
easy_words = [
    "cat", "dog", "sun", "bag", "rat", "bat", "pen", "cup", "man", "fan",
    "box", "car", "bed", "red", "top", "zip", "map", "pot", "cap", "log",
    "mat", "run", "net", "pin", "cut", "nap", "egg", "hit", "toy", "jam",
    "sit", "win", "lip", "fix", "kit", "tap", "hat", "pan", "tip", "mix",
    "ball", "tree", "star", "cake", "moon", "ship", "frog", "door", "gold",
    "fish", "book", "card", "bird", "fire", "lamp", "rock", "wind", "pear",
    "shoe", "coat", "seed", "ring", "time", "milk", "coin", "sand", "note",
    "hill", "leaf", "song", "desk", "rain", "wolf", "bear"
]
medium_words = [
    "apple", "baker", "candy", "dance", "eagle", "fruit", "grape", "house", "ideal",
    "jolly", "knock", "light", "magic", "noble", "ocean", "piano", "queen", "river",
    "spice", "table", "unity", "value", "wheat", "xenon", "yacht", "zebra", "angel",
    "blaze", "climb", "dream", "flame", "ghost", "heart", "island", "joker", "karma",
    "lunch", "mocha", "nurse", "orbit", "pride", "quiet", "realm", "sugar", "toast",
    "urban", "vivid", "water", "xerox", "yield", "zesty"
]
hard_words = [
    "ancient", "balloon", "captain", "diamond", "enclave", "fantasy", "gateway",
    "harmony", "insight", "journey", "kingdom", "lantern", "measure", "natural",
    "octopus", "picture", "quality", "rescue", "station", "thought", "unicorn",
    "victory", "welcome", "zealous", "admiral", "boulder", "crystal", "destiny",
    "freedom", "gallery", "history", "iceberg", "justice", "library", "mystery",
    "network", "opinion", "pattern", "rebuild", "sunrise", "tandem", "umbrella",
    "vulture", "whistle", "zealot", "aspiring", "bravery", "ceremony", "daydream"
]

#Word Levels
current_level = "easy"
words = {"easy": easy_words, "medium": medium_words, "hard": hard_words}
word_to_guess = random.choice(words[current_level])
scrambled_word = ''.join(random.sample(word_to_guess, len(word_to_guess)))
user_input = ""
hint_used = False

#Functions to Code

#Sound effects and Music(yet to be added)
def play_win_sound():
    """Plays a victory sound using a series of beeps."""
    winsound.Beep(1200, 1200)  # High-pitched beep
    winsound.Beep(1500, 1000)  # Higher-pitched beep
    winsound.Beep(1800, 1300)  # Even higher-pitched beep

def play_lost_sound():
    """Plays a defeat sound using a descending series of beeps."""
    winsound.Beep(800, 1300)   # Low-pitched beep
    winsound.Beep(600, 1200)   # Lower-pitched beep
    winsound.Beep(400, 1000)   # Even lower-pitched beep

def play_timer_ticking_sound(duration=5):
    end_time = time.time() + duration
    while time.time() < end_time:
        winsound.Beep(1000, 100)  # 1 kHz beep lasting 100ms
        time.sleep(0.9)

#scramble code (Returns Scrambled)
def scrambled_word_underscore(word):
    word_count = len(word)
    underscore_string = ""
    for i in range(word_count):
        underscore_string.append("_ ")
    return underscore_string

def scramble_word(word):
    word_list = list(word)  # Convert the word to a list of characters.
    random.shuffle(word_list)  # Shuffle the characters randomly.
    scrambled = ''.join(word_list)  # Join the shuffled characters back into a string.
    # Ensure the scrambled word isn't the same as the original.
    while scrambled == word:
        random.shuffle(word_list)
        scrambled = ''.join(word_list)
    return scrambled

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
        #Volume button and Restart button should be added here if was added
        screen.blit(pause_menu, (0, 0))
        pygame.display.flip()
        pygame.time.delay(5000)

def display_hint(screen,word_to_guess):
    pass
    # Drawing the hint button on screen

def display_score(screen, score):
    # Drawing the score button on screen
    font_size_score = 70
    font_score = pygame.font.Font("DJB Chalk It Up.ttf", font_size_score)
    score_text = font_score.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_text, (29,40))

#timer_function
def display_timer(screen , start_time, elapsed_time):
   #Drawing a timer on the screen
    font_size_timer = 98
    font_timer = pygame.font.Font("DJB Chalk It Up.ttf", font_size_timer)
    time_left_timer = max(0, start_time - elapsed_time)  # Ensure it doesn't go negative
    # Change color based on time
    color = (255,255,255) if time_left_timer > 10 else (255,0,0,)
    # Render the timer tex
    timer_text = font_timer.render(f"{int(time_left_timer)}", True, color)
    # Get the text's rectangle and center it on the screen
    timer_rect = timer_text.get_rect(center=(1137, 40))  # Adjust position as needed
    # Draw the text on the screen
    screen.blit(timer_text, timer_rect)
    return time_left

#Game over Function
def game_over(screen,score,font):
    font = pygame.font.Font("DJB Chalk It Up.ttf", 80)
    screen.blit(scaled_background, (0,0))
    over_text = font.render(f"Game Over ! Final Score: {score}", True,(255,255,255) )
    over_rect = over_text.get_rect(center = (640,300))
    screen.blit(over_text, over_rect)
    pygame.display.flip()
    pygame.time.delay(5000)

#game Loop
running = True

while running:
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Capture user input through the keyboard
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Check if the user presses Enter
                # Check if the guessed word is correct
                if user_input.lower() == word_to_guess.lower():
                    score += 10 if not hint_used else 5
                    current_level = 'medium' if score > 30 else "hard" if score > 60 else "easy"
                    word_to_guess = random.choice(words[current_level])
                    scrambled_word = scramble_word(word_to_guess)
                    user_input = ""
                    hint_used = False
                else:
                    score -= 1 # Penalize for wrong guess
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]  # Remove the last character
            elif event.key == pygame.K_ESCAPE:
                pause()
            elif event.key == pygame.K_QUESTION:
                hint_used = True
            else:
                user_input += event.unicode  # Add the typed character to user input

    screen.blit(scaled_background, (0, 0))
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

    # Call the timer function
    time_left = display_timer(screen, font, start_time, elapsed_time)

    #If hint used
    if hint_used:
        display_hint(screen,font,word_to_guess)

    # End the game when the timer reaches zero
    if time_left <= 0:
        running = False
        game_over(screen, score)
        print("Time's up!")  #prints in console

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)  # 30 FPS


    #Drawing the textures
    screen.blit(hint_button,(28, 578))
    screen.blit(pause_button, (1161, 609))
    scrambled_text = font.render(f"{scrambled_word}", True, (255, 255, 255))
    screen.blit(scrambled_text, (100, 200))
    user_input_text = font.render(f"Your Guess: {user_input}", True, (255, 255, 255))
    screen.blit(user_input_text, (100, 300))
    display_score(screen, font, score)

    # Draw the scaled background
    #screen.blit(scaled_background, (0, 0))

    # Update the display
    pygame.display.flip()

pygame.quit()





