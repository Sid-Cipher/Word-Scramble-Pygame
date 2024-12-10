import pygame

# Fixes and improvements for the provided Word Scramble game.

# Initialize Pygame and screen
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Word Scramble Game")

# Asset Paths (use placeholders if assets aren't available)
background_image_path = "/mnt/data/background.png"
hint_button_image_path = "/mnt/data/hint_button.png"
pause_button_image_path = "/mnt/data/pause_button.png"
background_music_path = "/mnt/data/background_music.mp3"
hint_sound_path = "/mnt/data/hint_sound.mp3"

# Colors and Fonts
white = (255, 255, 255)
black = (0, 0, 0)
font = pygame.font.Font(None, 36)

# Load and Handle Missing Assets
def safe_load_image(path, fallback_color=(200, 200, 200)):
    try:
        return pygame.image.load(path).convert_alpha()
    except pygame.error:
        return pygame.Surface((100, 50)).fill(fallback_color)

def safe_load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        return None

background_image = safe_load_image(background_image_path)
hint_button_image = safe_load_image(hint_button_image_path)
pause_button_image = safe_load_image(pause_button_image_path)
hint_sound = safe_load_sound(hint_sound_path)

# Placeholder music loading
try:
    pygame.mixer.music.load(background_music_path)
except pygame.error:
    pass  # Skip if music isn't available

# Helper to draw centered text
def draw_text_centered(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

# Game Variables
clock = pygame.time.Clock()
running = True
paused = False
score = 0
level = 1
scrambled_word = "PYTHON"
user_guess = ""
start_ticks = pygame.time.get_ticks()

# Main Game Loop
while running:
    screen.fill(black)
    screen.blit(background_image, (0, 0))

    # Check Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
            elif event.key == pygame.K_BACKSPACE:
                user_guess = user_guess[:-1]
            elif event.key == pygame.K_RETURN and not paused:
                if user_guess == "PYTHON":  # Correct word for testing
                    score += 1
                    level += 1
                    scrambled_word = "WINNER"
                user_guess = ""
            else:
                user_guess += event.unicode

    # Game Logic
    elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    if paused:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

    # Draw Game Elements
    draw_text_centered(screen, f"Score: {score}", font, white, 400, 50)
    draw_text_centered(screen, f"Level: {level}", font, white, 400, 100)
    draw_text_centered(screen, scrambled_word, font, white, 400, 200)
    draw_text_centered(screen, user_guess, font, white, 400, 300)
    draw_text_centered(screen, f"Time: {elapsed_seconds}s", font, white, 400, 400)

    # Draw Buttons
    screen.blit(hint_button_image, (50, 500))
    screen.blit(pause_button_image, (700, 500))

    # Refresh Screen
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
