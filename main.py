# I acknowledge the use of ChatGPT (GPT-5, OpenAI, https://chat.openai.com/) to assist in creating this file.

import pygame
import sys
import random

# Grid setup
CELL_SIZE = 100
GRID_WIDTH, GRID_HEIGHT = 10, 8  # larger grid
WIDTH, HEIGHT = GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE

# Colours
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 200, 0)
BG_COLOR = (25, 25, 25)
GRID_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)

def draw_grid(screen):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Escape – Grid AI")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 60)

    apple_x, apple_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
    snake_x, snake_y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)

    started = False
    running = True
    step_delay = 300  # ms between steps

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # --- Wait for arrow key to start ---
        if not started:
            screen.fill(BG_COLOR)
            title = font.render("Press Arrow Key to Start", True, TEXT_COLOR)
            rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(title, rect)
            pygame.display.flip()

            # Check for first arrow press
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                started = True
            continue

        # --- Player (apple) movement ---
        moved = False
        if keys[pygame.K_LEFT]:
            apple_x -= 1
            moved = True
        elif keys[pygame.K_RIGHT]:
            apple_x += 1
            moved = True
        elif keys[pygame.K_UP]:
            apple_y -= 1
            moved = True
        elif keys[pygame.K_DOWN]:
            apple_y += 1
            moved = True

        apple_x = max(0, min(GRID_WIDTH - 1, apple_x))
        apple_y = max(0, min(GRID_HEIGHT - 1, apple_y))

        # --- Snake AI (simple greedy) ---
        if snake_x < apple_x:
            snake_x += 1
        elif snake_x > apple_x:
            snake_x -= 1
        elif snake_y < apple_y:
            snake_y += 1
        elif snake_y > apple_y:
            snake_y -= 1

        # --- Collision detection ---
        if snake_x == apple_x and snake_y == apple_y:
            screen.fill(BG_COLOR)
            msg = font.render("Caught!", True, (255, 0, 0))
            rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(msg, rect)
            pygame.display.flip()
            pygame.time.wait(1500)
            running = False
            continue

        # --- Drawing ---
        screen.fill(BG_COLOR)
        draw_grid(screen)
        pygame.draw.rect(screen, APPLE_COLOR, (apple_x * CELL_SIZE, apple_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, SNAKE_COLOR, (snake_x * CELL_SIZE, snake_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()

        pygame.time.wait(step_delay)
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
