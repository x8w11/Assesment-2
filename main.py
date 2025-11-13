# I acknowledge the use of ChatGPT (GPT-5, OpenAI, https://chat.openai.com/) to assist in creating this file.

import pygame
import sys
import random

CELL_SIZE = 40
GRID_WIDTH, GRID_HEIGHT = 15, 12
WIDTH, HEIGHT = GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE

PLAYER_COLOR = (0, 0, 255)
SNAKE_COLOR = (0, 200, 0)
APPLE_COLOR = (255, 0, 0)
BG_COLOR = (25, 25, 25)
GRID_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)
CAUGHT_COLOR = (255, 0, 0)

NUM_APPLES = 3
STEP_DELAY = 200  # milliseconds per step


def draw_grid(screen):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))


def draw_text(screen, text, font, color, center):
    render = font.render(text, True, color)
    rect = render.get_rect(center=center)
    screen.blit(render, rect)


def random_empty_position(exclude):
    while True:
        pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        if pos not in exclude:
            return pos


def nearest_apple(snake_head, apples):
    return min(apples, key=lambda a: abs(a[0]-snake_head[0])+abs(a[1]-snake_head[1]))


def game_loop(screen, font):
    # Player
    player = (GRID_WIDTH//2, GRID_HEIGHT//2)

    # Snake initialization
    snake = [(random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))]

    # Random apples for snake
    apples = []
    for _ in range(NUM_APPLES):
        apples.append(random_empty_position(snake + [player]))

    started = False
    last_tick = pygame.time.get_ticks()
    score = 0

    # Player input direction
    player_dir = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_dir = "LEFT"
                    started = True
                elif event.key == pygame.K_RIGHT:
                    player_dir = "RIGHT"
                    started = True
                elif event.key == pygame.K_UP:
                    player_dir = "UP"
                    started = True
                elif event.key == pygame.K_DOWN:
                    player_dir = "DOWN"
                    started = True

        if not started:
            screen.fill(BG_COLOR)
            draw_text(screen, "Use Arrow Keys to Move", font, TEXT_COLOR, (WIDTH//2, HEIGHT//2))
            pygame.display.flip()
            continue

        current_time = pygame.time.get_ticks()
        if current_time - last_tick >= STEP_DELAY:
            last_tick = current_time

            # --- Player movement (per tick) ---
            if player_dir == "LEFT":
                player = (max(0, player[0]-1), player[1])
            elif player_dir == "RIGHT":
                player = (min(GRID_WIDTH-1, player[0]+1), player[1])
            elif player_dir == "UP":
                player = (player[0], max(0, player[1]-1))
            elif player_dir == "DOWN":
                player = (player[0], min(GRID_HEIGHT-1, player[1]+1))

            # --- Snake movement (greedy nearest apple) ---
            target = nearest_apple(snake[0], apples + [player])
            head_x, head_y = snake[0]
            if target[0] > head_x:
                head_x += 1
            elif target[0] < head_x:
                head_x -= 1
            elif target[1] > head_y:
                head_y += 1
            elif target[1] < head_y:
                head_y -= 1
            new_head = (head_x, head_y)

            # --- Collision checks ---
            if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT or new_head in snake:
                return score  # snake dies

            snake.insert(0, new_head)

            if new_head == player:
                return score  # snake caught player
            elif new_head in apples:
                apples.remove(new_head)
                apples.append(random_empty_position(snake + [player] + apples))
                score += 10  # grow snake by keeping tail
            else:
                snake.pop()  # remove tail if not eating

            score += 1

        # --- Draw everything ---
        screen.fill(BG_COLOR)
        draw_grid(screen)

        for apple in apples:
            pygame.draw.rect(screen, APPLE_COLOR, (apple[0]*CELL_SIZE, apple[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(screen, PLAYER_COLOR, (player[0]*CELL_SIZE, player[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for seg in snake:
            pygame.draw.rect(screen, SNAKE_COLOR, (seg[0]*CELL_SIZE, seg[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        draw_text(screen, f"Score: {score}", font, TEXT_COLOR, (100, 20))
        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Escape – Synchronized Tick")
    font = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()

    while True:
        score = game_loop(screen, font)

        # --- Game Over Screen ---
        screen.fill(BG_COLOR)
        draw_text(screen, "Caught!", font, CAUGHT_COLOR, (WIDTH//2, HEIGHT//2-30))
        draw_text(screen, f"Score: {score}", font, TEXT_COLOR, (WIDTH//2, HEIGHT//2+10))
        draw_text(screen, "Press R to Restart or Q to Quit", font, TEXT_COLOR, (WIDTH//2, HEIGHT//2+60))
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
