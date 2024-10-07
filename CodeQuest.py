import pygame
import time
import random
import sys

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# Define clock to control the game speed
clock = pygame.time.Clock()

# Define the snake size
SNAKE_BLOCK = 10

# Font settings
font_style = pygame.font.SysFont("bahnschrift", 25)

# Function to display score
def display_score(score):
    value = font_style.render("Score: " + str(score), True, WHITE)
    screen.blit(value, [0, 0])

# Function to draw the snake
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])

# Function to display the game over message
def game_over_message():
    font = pygame.font.SysFont("bahnschrift", 50)
    message = font.render("Game Over!", True, RED)
    screen.blit(message, [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3])
    pygame.display.update()
    time.sleep(2)

# Function to display the help menu
def display_help_menu():
    screen.fill(BLACK)
    help_text = [
        "Snake Game Help",
        "Use arrow keys to move the snake.",
        "Eat the red food to grow longer.",
        "Don't hit the walls or yourself.",
        "Press 'P' to pause, 'C' to continue.",
        "Press 'Q' to quit the game.",
        "Press 'C' to continue or 'M' for main menu."
    ]
    y_offset = 50
    for line in help_text:
        rendered_line = font_style.render(line, True, WHITE)
        screen.blit(rendered_line, (50, y_offset))
        y_offset += 40
    pygame.display.update()

# Main game loop
def game_loop():
    game_over = False
    game_close = False
    paused = False
    speed_selected = False
    game_help = False

    # Speed options (frames per second)
    speeds = {"Small": 10, "Medium": 15, "High": 25}
    speed = 15

    # Initial position of the snake
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    x_change = 0
    y_change = 0

    snake_list = []
    snake_length = 1

    food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    # Display speed selection menu
    while not speed_selected:
        screen.fill(BLACK)
        speed_text = [
            "Select Speed:",
            "1: Small",
            "2: Medium",
            "3: High",
            "Press H for Help"
        ]
        y_offset = 50
        for line in speed_text:
            rendered_line = font_style.render(line, True, WHITE)
            screen.blit(rendered_line, (SCREEN_WIDTH // 4, y_offset))
            y_offset += 40
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    speed = speeds["Small"]
                    speed_selected = True
                elif event.key == pygame.K_2:
                    speed = speeds["Medium"]
                    speed_selected = True
                elif event.key == pygame.K_3:
                    speed = speeds["High"]
                    speed_selected = True
                elif event.key == pygame.K_h:
                    game_help = True

        if game_help:
            display_help_menu()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        game_help = False
                        speed_selected = True
                    elif event.key == pygame.K_m:
                        game_help = False

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            game_over_message()
            display_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        # Pause logic
        while paused:
            screen.fill(BLACK)
            pause_message = font_style.render("Paused. Press 'C' to continue.", True, WHITE)
            screen.blit(pause_message, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 3))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -SNAKE_BLOCK
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = SNAKE_BLOCK
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -SNAKE_BLOCK
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = SNAKE_BLOCK
                    x_change = 0
                elif event.key == pygame.K_p:
                    paused = True

        if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
            game_close = True
        x += x_change
        y += y_change

        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, [food_x, food_y, SNAKE_BLOCK, SNAKE_BLOCK])

        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(SNAKE_BLOCK, snake_list)
        display_score(snake_length - 1)

        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            snake_length += 1

        clock.tick(speed)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
