import pygame
import time
import random
import winsound

# Initialize Pygame
pygame.init()

# Display Screen Width
screen = pygame.display.set_mode((1280, 720))

# Title and Icon
pygame.display.set_caption("Word Scramble")
icon = pygame.image.load('crossword.png')
pygame.display.set_icon(icon)

# Loading Assets
hint_button = pygame.image.load("hint_button.png")
hint_button = pygame.transform.scale(hint_button, (110, 132))
pause_button = pygame.image.load("pause_button.png")
pause_button = pygame.transform.scale(pause_button, (62, 70))
pause_menu = pygame.image.load("Pause_menu.png")
pause_menu = pygame.transform.scale(pause_menu, (1280, 720))

background = pygame.image.load("background.png")
scaled_background = pygame.transform.scale(background, (1280, 720))

# Fonts
font_size = 40
try:
    font = pygame.font.Font("DJB Chalk It Up.ttf", font_size)
except FileNotFoundError:
    font = pygame.font.SysFont(None, font_size)

# Timer
start_time = 30
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()

# Score system
score = 1647

# Words
words = {
    "easy": ["cat", "dog", "sun", "bag", "rat"],
    "medium": ["apple", "baker", "candy"],
    "hard": ["ancient", "balloon", "captain"]
}

current_level = "easy"
word_to_guess = random.choice(words[current_level])
scrambled_word = ''.join(random.sample(word_to_guess, len(word_to_guess)))
user_input = ""
hint_used = False


def scramble_word(word):
    scrambled = ''.join(random.sample(word, len(word)))
    while scrambled == word:
        scrambled = ''.join(random.sample(word, len(word)))
    return scrambled


def display_timer(screen, font, start_time, elapsed_time):
    font_size_timer = 98
    font_timer = pygame.font.Font("DJB Chalk It Up.ttf", font_size_timer)
    time_left = max(0, start_time - elapsed_time)
    color = (255, 255, 255) if time_left > 10 else (255, 0, 0)
    timer_text = font_timer.render(f"{int(time_left)}", True, color)
    timer_rect = timer_text.get_rect(center=(1137, 40))
    screen.blit(timer_text, timer_rect)


def game_over(screen, score):
    font = pygame.font.Font("DJB Chalk It Up.ttf", 80)
    screen.blit(scaled_background, (0, 0))
    over_text = font.render(f"Game Over! Final Score: {score}", True, (255, 255, 255))
    over_rect = over_text.get_rect(center=(640, 300))
    screen.blit(over_text, over_rect)
    pygame.display.flip()
    pygame.time.delay(5000)


running = True
while running:
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if user_input.lower() == word_to_guess.lower():
                    score += 10 if not hint_used else 5
                    current_level = (
                        "medium" if score > 30
                        else "hard" if score > 60
                        else "easy"
                    )
                    word_to_guess = random.choice(words[current_level])
                    scrambled_word = scramble_word(word_to_guess)
                    user_input = ""
                    hint_used = False
                else:
                    score -= 1
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            elif event.key == pygame.K_ESCAPE:
                paused = True
                while paused:
                    for e in pygame.event.get():
                        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                            paused = False
                    screen.blit(pause_menu, (0, 0))
                    pygame.display.update()

    screen.blit(scaled_background, (0, 0))
    screen.blit(hint_button, (28, 578))
    screen.blit(pause_button, (1161, 609))

    scrambled_text = font.render(f"Scrambled: {scrambled_word}", True, (255, 255, 255))
    screen.blit(scrambled_text, (100, 200))
    user_input_text = font.render(f"Your Guess: {user_input}", True, (255, 255, 255))
    screen.blit(user_input_text, (100, 300))

    display_timer(screen, font, start_time, elapsed_time)

    if elapsed_time >= start_time:
        running = False
        game_over(screen, score)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
