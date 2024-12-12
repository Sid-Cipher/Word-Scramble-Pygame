import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_ROWS, GRID_COLS = 6, 6
CELL_SIZE = 80
FONT = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (200, 200, 200)

# Global variables
score = 0
max_score = 0
current_level = 1
game_timer = 30  # Timer in seconds
match_pairs = [(2, 2), (3, 4)]  # Pairs for each level

def generate_grid(target_pair):
    grid = [[random.randint(1, 9) for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    # Replace two random cells with target pair
    pair_positions = random.sample(range(GRID_ROWS * GRID_COLS), 2)
    r1, c1 = divmod(pair_positions[0], GRID_COLS)
    r2, c2 = divmod(pair_positions[1], GRID_COLS)
    grid[r1][c1] = target_pair[0]
    grid[r2][c2] = target_pair[1]
    return grid

def check_pair(grid, selected_cells, target_pair):
    if len(selected_cells) == 2:
        r1, c1 = selected_cells[0]
        r2, c2 = selected_cells[1]
        if (grid[r1][c1], grid[r2][c2]) == target_pair or (grid[r2][c2], grid[r1][c1]) == target_pair:
            return True
    return False

def remove_pair(grid, selected_cells):
    for r, c in selected_cells:
        grid[r][c] = 0

def display_score(screen, level_score, max_score):
    level_text = FONT.render(f"Score: {level_score}", True, BLACK)
    max_text = FONT.render(f"Max Score: {max_score}", True, BLACK)
    screen.blit(level_text, (10, 10))
    screen.blit(max_text, (10, 50))

def all_pairs_removed(grid, target_pair):
    for row in grid:
        if row.count(target_pair[0]) >= 2:
            return False
    return True

def display_timer(screen, time_left):
    timer_text = FONT.render(f"Time Left: {time_left}s", True, BLACK)
    screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))

def next_level(screen, clock):
    global current_level, score, game_timer
    if current_level == 1:
        target_pair = match_pairs[0]
    elif current_level == 2:
        target_pair = match_pairs[1]
    else:
        return False  # End of game

    grid = generate_grid(target_pair)
    selected_cells = []
    start_time = time.time()

    while True:
        screen.fill(WHITE)

        # Draw grid
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                num = grid[r][c]
                rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, LIGHT_GRAY, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)
                if num != 0:
                    text = FONT.render(str(num), True, BLACK)
                    screen.blit(text, (rect.x + 30, rect.y + 20))

        # Display instructions
        instruction_text = FONT.render(f"Find pairs of {target_pair}", True, BLACK)
        screen.blit(instruction_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50))

        # Display score and timer
        display_score(screen, score, max_score)
        display_timer(screen, game_timer - int(time.time() - start_time))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                c, r = x // CELL_SIZE, y // CELL_SIZE
                if 0 <= r < GRID_ROWS and 0 <= c < GRID_COLS and grid[r][c] != 0:
                    selected_cells.append((r, c))
                    if len(selected_cells) == 2:
                        if check_pair(grid, selected_cells, target_pair):
                            remove_pair(grid, selected_cells)
                            score += 5
                            selected_cells = []
                        else:
                            selected_cells = []

        if all_pairs_removed(grid, target_pair):
            break

        # If timer ends, break to the next level
        if time.time() - start_time >= game_timer:
            break

        pygame.display.flip()
        clock.tick(30)

    current_level += 1
    return True

# Main game loop
def game_loop():
    global score, max_score

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Number Match Game")

    clock = pygame.time.Clock()

    while next_level(screen, clock):
        pass

    # After second level, wait for 30 seconds before ending
    end_time = time.time()
    while time.time() - end_time < 30:
        screen.fill(WHITE)
        display_score(screen, score, max_score)
        display_timer(screen, 30 - int(time.time() - end_time))
        pygame.display.flip()
        clock.tick(30)

    # Display final score
    print(f"Final Score: {score}")
    if score > max_score:
        max_score = score
    print(f"Max Score: {max_score}")

# Run the game
game_loop()
pygame.quit()
