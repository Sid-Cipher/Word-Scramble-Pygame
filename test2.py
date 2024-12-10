import pygame
import time

# Initialize Pygame and the Mixer
pygame.init()
pygame.mixer.init()

# Load and play music
pygame.mixer.music.load("Lukrembo.mp3")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)  # Play indefinitely

# Run a dummy game loop
try:
    while True:
        time.sleep(1)  # Keep the program running to hear the music
except KeyboardInterrupt:
    pygame.mixer.music.stop()
    print("Music stopped. Game over!")
