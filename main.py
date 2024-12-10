import pygame
import time
import random
import winsound

#Initialziing the Pygame
pygame.init()
pygame.mixer.init()

# Load and play music
pygame.mixer.music.load("Lukrembo.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)  # Play indefinitely

#Loading sound effects
win_sound = pygame.mixer.Sound("correct_ans.wav")
lose_sound = pygame.mixer.Sound("lost_sound_effect.mp3")
hint_sound = pygame.mixer.Sound("hint.wav")
pause_sound = pygame.mixer.Sound("pause.mp3")
unpause_sound = pygame.mixer.Sound("unpause.mp3")
score_sound = pygame.mixer.Sound("Score_card.wav")

# Adjust volumes for sound effects
win_sound.set_volume(0.5)
lose_sound.set_volume(0.5)
hint_sound.set_volume(0.5)
pause_sound.set_volume(0.5)
unpause_sound.set_volume(0.5)
score_sound.set_volume(0.5)

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
font_size = 80
try:
    font = pygame.font.Font("DJB Chalk It Up.ttf", font_size)
except FileNotFoundError:
    font = pygame.font.SysFont(None, font_size)

font_size_scrambled = 65
try:
    font_scrambled = pygame.font.Font("DJB Chalk It Up.ttf", font_size_scrambled)
except FileNotFoundError:
    font_scrambled = pygame.font.SysFont(None, font_size_scrambled)

# Timer 🕛
start_time = 31  # Start with 30 seconds
time_left = start_time
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()  # Record the starting tick (in milliseconds)

# Score system
score = 0

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
"""def play_win_sound():
    winsound.Beep(1200, 1200)  # High-pitched beep
    winsound.Beep(1500, 1000)  # Higher-pitched beep
    winsound.Beep(1800, 1300)  # Even higher-pitched beep

def play_lost_sound():
    winsound.Beep(800, 1300)   # Low-pitched beep
    winsound.Beep(600, 1200)   # Lower-pitched beep
    winsound.Beep(400, 1000)   # Even lower-pitched beep

def play_timer_ticking_sound(duration=5):
    end_time = time.time() + duration
    while time.time() < end_time:
        winsound.Beep(1000, 100)  # 1 kHz beep lasting 100ms
        time.sleep(0.9)"""

#scramble code (Returns Scrambled)
def scrambled_word_underscore(word):
    word_count = len(word)
    underscore_string = ""
    for i in range(word_count):
        underscore_string.append("_ ")
    return underscore_string

def scramble_word(word):
    scrambled = ''.join(random.sample(word, len(word)))
    while scrambled == word:
        scrambled = ''.join(random.sample(word, len(word)))
    return scrambled

def pause():
    global timer_paused, start_ticks
    timer_paused = True
    paused_start_ticks = pygame.time.get_ticks()  # Record the time when paused
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Unpause on ESC
                    sound_effect_play("unpause_sound")
                    paused = False
                    timer_paused = False
                    # Adjust start_ticks to compensate for paused time
                    paused_duration = pygame.time.get_ticks() - paused_start_ticks
                    start_ticks += paused_duration
        screen.blit(pause_menu, (0, 0))
        pygame.display.flip()
        clock.tick(30)  # Limit the frame rate during pause

def music_play():
    try: # Load and play music
        pygame.mixer.music.load("Lukrembo.mp3")
        pygame.mixer.music.set_volume(0.02)
        pygame.mixer.music.play(-1)  # Play indefinitely
    except pygame.error as e:
        print(f"Error loading music file. Exception: {e}")

def sound_effect_play(effect):
    try:
        if effect == "hint_sound":
            pygame.mixer.Sound.play(hint_sound)
        elif effect == "pause_sound":
            pygame.mixer.Sound.play(pause_sound)
        elif effect == "unpause_sound":
            pygame.mixer.Sound.play(unpause_sound)
        elif effect == "score_sound":
            pygame.mixer.Sound.play(score_sound)
        elif effect == "lose_sound":
            pygame.mixer.Sound.play(lose_sound)
        elif effect == "win_sound":
            pygame.mixer.Sound.play(win_sound)
    except pygame.error as e:
        print(f"Error loading music file. Exception: {e}")

def display_hint(screen, word_to_guess):
    hint_letter = random.choice(word_to_guess)
    hint_text = font.render(f"Hint: Includes '{hint_letter}'", True, (255, 255, 255))
    screen.blit(hint_text, (100, 400))  # Adjust position as needed

def display_score(screen, score):
    # Drawing the score button on screen
    font_size_score = 70
    font_score = pygame.font.Font("DJB Chalk It Up.ttf", font_size_score)
    score_text = font_score.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_text, (29,40))

#timer_function
def display_timer(screen , start_time, elapsed_time):
   #Drawing a timer on the screen
    font_size_timer = 90
    font_timer = pygame.font.Font("DJB Chalk It Up.ttf", font_size_timer)
    time_left_timer = max(0, start_time - elapsed_time)  # Ensure it doesn't go negative
    # Change color based on time
    color = (255,255,255) if time_left_timer > 10 else (255,0,0,)
    # Render the timer tex
    timer_text = font_timer.render(f"{int(time_left_timer)}", True, color)
    # Get the text's rectangle and center it on the screen
    timer_rect = timer_text.get_rect(center=(1137, 70))  # Adjust position as needed
    # Draw the text on the screen
    screen.blit(timer_text, timer_rect)
    return time_left_timer

#Game over Function
def game_over(screen, score):
    font = pygame.font.Font("DJB Chalk It Up.ttf", 80)
    screen.blit(scaled_background, (0, 0))
    over_text = font.render(f"Game Over! Final Score: {score}", True, (255, 255, 255))
    over_rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(over_text, over_rect)
    pygame.display.flip()
    pygame.time.delay(5000)  # Show for 5 seconds before closing


#game Loop
running = True
timer_paused = False

while running:

    if not timer_paused:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # Time in seconds
    else:
        start_ticks = pygame.time.get_ticks()
        elapsed_time = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Capture user input through the keyboard
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Check if the user presses Enter
                # Check if the guessed word is correct
                if user_input.lower() == word_to_guess.lower():
                    start_ticks = pygame.time.get_ticks()
                    sound_effect_play("win_sound")
                    if current_level == 'easy':
                        score += 10 if not hint_used else 5
                    elif current_level == 'medium':
                        score += 20 if not hint_used else 10
                    elif current_level == "hard":
                        score += 30 if not hint_used else 15
                    current_level = 'medium' if score > 100 else "hard" if score > 300 else "easy"
                    pygame.time.delay(500)
                    word_to_guess = random.choice(words[current_level])
                    scrambled_word = scramble_word(word_to_guess)
                    user_input = ""
                    hint_used = False
                else:
                    sound_effect_play("lose_sound")
                    if score > 0:
                        score -= 1 # Penalize for wrong guess
                    else:
                        score = 0
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]  # Remove the last character
            elif event.key == pygame.K_ESCAPE:
                sound_effect_play("pause_sound")
                pause()
            elif event.unicode == '?':
                sound_effect_play("hint_sound")
                hint_used = True
                display_hint(screen,word_to_guess)
            else:
                user_input += event.unicode  # Add the typed character to user input

    screen.blit(scaled_background, (0, 0))
    #Draw the hint button and pause button
    screen.blit(hint_button, (28, 578))
    screen.blit(pause_button, (1161,609))

    # Screen width (assuming a window of 1280, modify as per your screen width)
    screen_width = 1280
    x_pos = 147
    y_pos = 240
    spacing_scrambled = 36  # Adjust this value to control space between words

    x_pos_un = 376
    y_pos_un = 445
    spacing_unscrambled = 18  # Adjust this value to control space between words



    # Function to calculate the total width of the text
    def calculate_total_text_width(words, font, spacing):
        total_width = 0
        for word in words:
            word_text = font.render(word, True, (255, 255, 255))  # Render the word
            total_width += word_text.get_width() + spacing
        return total_width


    # Calculate the total width of the words (for both user_input and scrambled_word)
    total_user_input_width = calculate_total_text_width(user_input, font, spacing_scrambled)
    total_scrambled_word_width = calculate_total_text_width(scrambled_word, font_scrambled, spacing_unscrambled)

    # Calculate starting positions for centering
    x_pos = (screen_width - total_user_input_width + spacing_scrambled) // 2
    x_pos_un = (screen_width - total_scrambled_word_width + spacing_unscrambled) // 2

    # Adjust vertical position for underscores (for example, 25 pixels below the words)
    underscore_offset = 25  # Adjusted to 25px gap below the words

    # Render and display the words centered with underscores
    for word in user_input:
        word_text = font.render(word, True, (255, 255, 255))  # White color text
        screen.blit(word_text, (x_pos, y_pos))

        # Render the underscore below the word
        underscore_text = font.render("_" * len(word), True, (255, 255, 255))  # Underscores same length as word
        screen.blit(underscore_text, (x_pos, y_pos + underscore_offset))  # Place it 25px below the word

        x_pos += word_text.get_width() + spacing_scrambled

    # Render scrambled words without underscores below them
    for word in scrambled_word:
        word_text = font_scrambled.render(word, True, (255, 255, 255))  # White color text
        screen.blit(word_text, (x_pos_un, y_pos_un))

        x_pos_un += word_text.get_width() + spacing_unscrambled

    # Draw the scrambled word on the screen

      # Adjust position as needed
    # Draw user input on the screen
      # Adjust position as needed
    # Calculate elapsed time
    current_ticks = pygame.time.get_ticks()
    elapsed_time = (current_ticks - start_ticks) / 1000  # Convert milliseconds to seconds
    # Clear the screen and draw the background

    # Call the timer function
    time_left = display_timer(screen, start_time, elapsed_time)

    # End the game when the timer reaches zero
    if time_left <= 0:
        running = False
        sound_effect_play("score_sound")
        game_over(screen, score)
        print("Time's up!")  #prints in console

    # Cap the frame rate
    clock.tick(30)  # 30 FPS

    #Drawing the textures
    screen.blit(hint_button,(28, 578))
    screen.blit(pause_button, (1161, 609))
    display_score(screen,score)

    # Draw the scaled background
    #screen.blit(scaled_background, (0, 0))

    # Update the display
    pygame.display.flip()


pygame.quit()





