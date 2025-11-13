# I acknowledge the use of ChatGPT (GPT-5, OpenAI, https://chat.openai.com/) to assist in creating this file.

import pygame
import sys
import random

CELL_SIZE = 100
GRID_WIDTH, GRID_HEIGHT = 10, 8
WIDTH, HEIGHT = GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE

APPLE_COLOR = (255, 0, 0)
EXTRA_APPLE_COLOR = (255, 150, 0)
SNAKE_COLOR = (0, 200, 0)
BG_COLOR = (25, 25, 25)
GRID_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)
CAUGHT_COLOR = (255, 0, 0)

NUM_EXTRA_APPLES = 3  # number of random apples on the field


def draw_grid(screen):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))


def draw_text(screen, text, font, color, center):
    render = font.render(text, True, color)
    rect = render.get_rect(center=center)
    screen.blit(render, rect)


def random_empty_position(exclude_positions):
    """Generate a random (x, y) not in excluded list."""
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in exclude_positions:
            return pos


def game_loop(screen, font):
    apple_x, apple_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
    snake_x, snake_y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
    started = False
    score = 0
    step_delay = 300
    running = True

    # --- Spawn extra apples ---
    extra_apples = []
    for _ in range(NUM_EXTRA_APPLES):
        pos = random_empty_position([(apple_x, apple_y), (snake_x, snake_y)])
        extra_apples.append(pos)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # --- Wait for start ---
        if not started:
            screen.fill(BG_COLOR)
            draw_text(screen, "Press Arrow Key to Start", font, TEXT_COLOR, (WIDTH // 2, HEIGHT // 2))
            pygame.display.flip()
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                started = True
            continue

        # --- Player movement ---
        if keys[pygame.K_LEFT]:
            apple_x -= 1
        elif keys[pygame.K_RIGHT]:
            apple_x += 1
        elif keys[pygame.K_UP]:
            apple_y -= 1
        elif keys[pygame.K_DOWN]:
            apple_y += 1

        apple_x = max(0, min(GRID_WIDTH - 1, apple_x))
        apple_y = max(0, min(GRID_HEIGHT - 1, apple_y))

        # --- Snake AI ---
        if snake_x < apple_x:
            snake_x += 1
        elif snake_x > apple_x:
            snake_x -= 1
        elif snake_y < apple_y:
            snake_y += 1
        elif snake_y > apple_y:
            snake_y -= 1

        # --- Snake catches player apple ---
        if snake_x == apple_x and snake_y == apple_y:
            return score  # Game over

        # --- Player apple eats extra apples ---
        for i, (ex, ey) in enumerate(extra_apples):
            if ex == apple_x and ey == apple_y:
                score += 10  # give bigger score for collecting
                new_pos = random_empty_position(extra_apples + [(apple_x, apple_y), (snake_x, snake_y)])
                extra_apples[i] = new_pos

        # --- Draw everything ---
        screen.fill(BG_COLOR)
        draw_grid(screen)

        # Draw all extra apples
        for ex, ey in extra_apples:
            pygame.draw.rect(screen, EXTRA_APPLE_COLOR, (ex * CELL_SIZE, ey * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw player apple and snake
        pygame.draw.rect(screen, APPLE_COLOR, (apple_x * CELL_SIZE, apple_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, SNAKE_COLOR, (snake_x * CELL_SIZE, snake_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        draw_text(screen, f"Score: {score}", font, TEXT_COLOR, (100, 40))
        pygame.display.flip()

        score += 1
        pygame.time.wait(step_delay)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Escape – Multi-Apple Mode")
    font = pygame.font.SysFont(None, 60)
    clock = pygame.time.Clock()

    while True:
        score = game_loop(screen, font)

        # --- Game Over Screen ---
        screen.fill(BG_COLOR)
        draw_text(screen, "Caught!", font, CAUGHT_COLOR, (WIDTH // 2, HEIGHT // 2 - 50))
        draw_text(screen, f"Score: {score}", font, TEXT_COLOR, (WIDTH // 2, HEIGHT // 2 + 10))
        draw_text(screen, "Press R to Restart or Q to Quit", font, TEXT_COLOR, (WIDTH // 2, HEIGHT // 2 + 80))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()
            if keys[pygame.K_r]:
                waiting = False
            clock.tick(15)


if __name__ == "__main__":
    main()
