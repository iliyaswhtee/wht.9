import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
SNAKE_SPEED = 10
LEVEL_UP_SCORE = 3  # Score needed to level up

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize game variables
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

snake = [(WIDTH // 2, HEIGHT // 2)]
food = [(random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE, random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE, random.randint(1, 5), time.time())]  # Add weight and creation time
score = 0
level = 1  # Add level variable
direction = 'RIGHT'

# Main game loop
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != 'DOWN':
        direction = 'UP'
    if keys[pygame.K_DOWN] and direction != 'UP':
        direction = 'DOWN'
    if keys[pygame.K_LEFT] and direction != 'RIGHT':
        direction = 'LEFT'
    if keys[pygame.K_RIGHT] and direction != 'LEFT':
        direction = 'RIGHT'

    # Snake move
    x, y = snake[0]
    if direction == 'UP':
        y -= GRID_SIZE
    if direction == 'DOWN':
        y += GRID_SIZE
    if direction == 'LEFT':
        x -= GRID_SIZE
    if direction == 'RIGHT':
        x += GRID_SIZE

    # Check for collision with walls or itself
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or (x, y) in snake:
        pygame.quit()
        quit()

    snake.insert(0, (x, y))

    # Check if snake eats the food
    for f in food:
        if (x, y) == (f[0], f[1]):
            score += f[2]  # Add the food's weight to the score
            food.remove(f)
            # Level up if score is high enough
            if score % LEVEL_UP_SCORE == 0:
                level += 1
            break
    else:
        snake.pop()

    # Generate new food
    if random.random() < 0.02:  # 2% chance per frame
        food.append((random.randint(0, WIDTH // GRID_SIZE - 1) * GRID_SIZE, random.randint(0, HEIGHT // GRID_SIZE - 1) * GRID_SIZE, random.randint(1, 5), time.time()))

    # Remove old food
    for f in food:
        if time.time() - f[3] > 10:  # 10 seconds
            food.remove(f)

    # Draw the snake
    for s in snake:
        pygame.draw.rect(screen, GREEN, (s[0], s[1], GRID_SIZE, GRID_SIZE))

    # Draw the food
    for f in food:
        pygame.draw.rect(screen, RED, (f[0], f[1], GRID_SIZE, GRID_SIZE))

    # Display the score and level
    font = pygame.font.SysFont(None, 30)
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    level_text = font.render("Level: " + str(level), True, (0, 0, 0))  # Add level display
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))  # Adjust position for level display

    pygame.display.update()
    clock.tick(SNAKE_SPEED + level)  # Increase speed with level