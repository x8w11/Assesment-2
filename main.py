# I acknowledge the use of ChatGPT (GPT-5, OpenAI, https://chat.openai.com/) to assist in creating this file.

import pygame
import sys

# Constants
WIDTH, HEIGHT = 640, 480
APPLE_SIZE = 20
APPLE_SPEED = 5
BG_COLOR = (30, 30, 30)
APPLE_COLOR = (255, 0, 0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Escape")

    clock = pygame.time.Clock()

    # Player (apple) start position
    apple_x, apple_y = WIDTH // 2, HEIGHT // 2

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Key handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            apple_x -= APPLE_SPEED
        if keys[pygame.K_RIGHT]:
            apple_x += APPLE_SPEED
        if keys[pygame.K_UP]:
            apple_y -= APPLE_SPEED
        if keys[pygame.K_DOWN]:
            apple_y += APPLE_SPEED

        # Boundaries
        apple_x = max(0, min(WIDTH - APPLE_SIZE, apple_x))
        apple_y = max(0, min(HEIGHT - APPLE_SIZE, apple_y))

        # Draw
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, APPLE_COLOR, (apple_x, apple_y, APPLE_SIZE, APPLE_SIZE))
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
