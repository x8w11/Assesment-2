# I acknowledge the use of ChatGPT (GPT-5, OpenAI, https://chat.openai.com/) to assist in creating this file.

import pygame
import sys

# Grid constants
CELL_SIZE = 100
GRID_WIDTH, GRID_HEIGHT = 6, 4   # 6x4 grid -> 600x400 window
WIDTH, HEIGHT = GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE

APPLE_COLOR = (255, 0, 0)
BG_COLOR = (30, 30, 30)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Escape (Grid Version)")

    clock = pygame.time.Clock()

    # Player (apple) starts at center cell
    apple_x, apple_y = GRID_WIDTH // 2, GRID_HEIGHT // 2

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
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

        # Clamp within grid bounds
        apple_x = max(0, min(GRID_WIDTH - 1, apple_x))
        apple_y = max(0, min(GRID_HEIGHT - 1, apple_y))

        # Redraw
        screen.fill(BG_COLOR)

        # Draw grid lines
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, (50, 50, 50), (0, y), (WIDTH, y))

        # Draw apple
        rect = pygame.Rect(apple_x * CELL_SIZE, apple_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, APPLE_COLOR, rect)

        pygame.display.flip()

        # Slow down to grid pace
        if moved:
            pygame.time.wait(200)  # 200ms delay for grid steps

        clock.tick(30)

if __name__ == "__main__":
    main()
