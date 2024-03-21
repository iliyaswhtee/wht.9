# Import modules
import pygame
import sys
from pygame.locals import *
import random
import time

# Initialize pygame
pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SPEED = 5 # start speed
SCORE = 0
COINS_COLLECTED = 0
N = 10  # Number of coins to collect before increasing speed

# Fonts that we use
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 40)
game_over = font.render("Game Over", True, BLACK)
background = pygame.image.load("C:\pp2 lab 8\sup.jpg")

# Set display screen
DISPLAYSURF = pygame.display.set_mode((600, 800))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Traffic Race")

# Now we open different classes for each feature and write their functions
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:\pp2 lab 8\images.png")
        self.rect = self.image.get_rect()
        self.rect.center = (200, 650)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.rect.move_ip(-SPEED, 0)
        if keys[K_RIGHT]:
            self.rect.move_ip(SPEED, 0)
        if keys[K_UP]:
            self.rect.move_ip(0, -SPEED)
        if keys[K_DOWN]:
            self.rect.move_ip(0, SPEED)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:\pp2 lab 8\kollil.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.speed = SPEED

    def move(self):
        global SCORE
        self.rect.move_ip(0, self.speed)
        if self.rect.top > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self, image_path, points):
        super().__init__()
        self.image = pygame.image.load(image_path) 
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.points = points

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

P1 = Player()  # Create player
E1 = Enemy()  # Create enemy
# Create two types of coins
C1 = Coin("C:\pp2 lab 8\lkjjj.png", 1)  # Basic coin
C2 = Coin("C:\pp2 lab 9\kijkl.png", 3)  # Special coin

enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group() 
coins.add(C1)
coins.add(C2)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)
all_sprites.add(C2)

# Speed
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Fonts and their collor i use black
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    coins_collected = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_collected, (400, 10))

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

# Sound if we collide with enemy car
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("C:\pp2 lab 8\katja-lel-mojj-marmeladnyjj.mp3").play()
        time.sleep(0)
        DISPLAYSURF.fill(GREEN)
        DISPLAYSURF.blit(game_over, (130, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(3)
        pygame.quit()
        sys.exit()
    if pygame.sprite.spritecollideany(P1, coins):
        for coin in coins: 
            if pygame.sprite.collide_rect(P1, coin):
                COINS_COLLECTED += coin.points  # Add the coin's points to the total
                coin.rect.top = 0
                coin.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        if COINS_COLLECTED % N == 0: #collected coins
            for enemy in enemies:
                enemy.speed += 1 # increase the speed for 1 for every 10 coins
    pygame.display.update()
    FramePerSec.tick(FPS)