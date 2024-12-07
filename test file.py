import pygame
import random

# Initialize Pygame
pygame.init()

# Display Screen Width
screen = pygame.display.set_mode((1280, 720))

# Title and Icon
pygame.display.set_caption("Word Scramble")
icon = pygame.image.load("crossword.png")
pygame.display.set_icon(icon)

# Load Assets
hint_button = pygame.image.load("hint_button.png")
hint_button = pygame.transform.scale(hint_button, (110, 132))
pause_button = pygame.image.load("pause_button.png")
pause_button = pygame.transform.scale(pause_button, (62, 70))
background = pygame.image.load("background.png")
scaled_background = pygame.transform.scale(background, (1280, 720))

# Font Setup
font_size = 40
font = pygame.font.Font("DJB Chalk It Up.ttf", font_size)

# Timer
start_time = 30
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()

# Score System
score = 0

# Word Levels
easy_words = ["cat", "dog", "bat"]
medium_words = ["apple", "grape", "house"]
hard_words = ["elephant", "umbrella", "happiness"]
current_level = "easy"
words = {"easy": easy_words, "medium": medium_words, "hard": hard_words}
word_to_guess = random.choice(words[current_level])
scrambled_word = ''.join(random.sample(word_to_guess, len(word_to_guess)))
user_input = ""
hint_used = False

# Scramble Function
def scramble_word(word):
    word_list = list(word)
    random.shuffle(word_list)
    scrambled = ''.join(word_list)
    while scrambled == word:
        random.shuffle(word_list)
        scrambled = ''.join(word_list)
    return scrambled

# Timer Function
def display_timer(screen, font, start_time, elapsed_time):
    font_size = 98
    font = pygame.font.Font("DJB Chalk It Up.ttf", font_size)
    time_left = max(0, start_time - elapsed_time)
    color = (255, 255, 255) if time_left > 10 else (255, 0, 0)
    timer_text = font.render(f"{int(time_left)}", True, color)
    timer_rect = timer_text.get_rect(center=(1137, 40))
    screen.blit(timer_text, timer_rect)
    return time_left

# Display Score
def display_score(screen, font, score):
    score_text = font.render(f"Score: {score}", True, (255, 255, 0))
    screen.blit(score_text, (1000, 40))

# Display Hint
def display_hint(screen, font, word):
    hint_text = font.render(f"Hint: {word[0]}...", True, (0, 255, 0))
    screen.blit(hint_text, (100, 500))

# Pause Functionality
def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
        font = pygame.font.Font("DJB Chalk It Up.ttf", 80)
        pause_text = font.render("Game Paused. Press P to Resume.", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(640, 360))
        screen.blit(scaled_background, (0, 0))
        screen.blit(pause_text, pause_rect)
        pygame.display.flip()

# Game Over Screen
def game_over(screen, score):
    font = pygame.font.Font("DJB Chalk It Up.ttf", 80)
    screen.fill((0, 0, 0))
    over_text = font.render(f"Game Over! Final Score: {score}", True, (255, 255, 255))
    over_rect = over_text.get_rect(center=(640, 300))
    screen.blit(over_text, over_rect)
    pygame.display.flip()
    pygame.time.delay(3000)

# Game Loop
running = True
while running:
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if user_input.lower() == word_to_guess.lower():
                    score += 10 if not hint_used else 5  # Fewer points if hint is used
                    current_level = "medium" if score > 30 else "hard" if score > 60 else "easy"
                    word_to_guess = random.choice(words[current_level])
                    scrambled_word = scramble_word(word_to_guess)
                    user_input = ""
                    hint_used = False
                else:
                    score -= 1  # Penalize for wrong guess
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            elif event.key == pygame.K_p:
                pause_game()
            elif event.key == pygame.K_h:  # Hint key
                hint_used = True
            else:
                user_input += event.unicode

    # Draw Everything
    screen.blit(scaled_background, (0, 0))
    screen.blit(hint_button, (28, 578))
    screen.blit(pause_button, (1161, 609))
    scrambled_text = font.render(f"Scrambled: {scrambled_word}", True, (255, 255, 255))
    screen.blit(scrambled_text, (100, 200))
    user_input_text = font.render(f"Your Guess: {user_input}", True, (255, 255, 255))
    screen.blit(user_input_text, (100, 300))
    display_score(screen, font, score)

    # Display Hint if used
    if hint_used:
        display_hint(screen, font, word_to_guess)

    # Timer
    time_left = display_timer(screen, font, start_time, elapsed_time)

    # End Game Condition
    if time_left <= 0:
        running = False
        game_over(screen, score)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
