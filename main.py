# Tutorial by Coding With Russ
# https://www.youtube.com/watch?v=mqz1_wRSMwo&ab_channel=CodingWithRuss
# Game created by Steven Theron
# 9 October 2023

import pygame
from pygame import mixer
from pygame.locals import *
import random

from Spaceship import Spaceship
from Aliens import Aliens
from AlienBullets import AlienBullets

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

# Define fps
clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Fonts
pygame.font.init()
font30 = pygame.font.SysFont("Constantia", 30)
font40 = pygame.font.SysFont("Constantia", 40)

# Load Game Assets
bg = pygame.image.load("assets/background1.png")

# Load sounds
explosion_fx1 = pygame.mixer.Sound("assets/sounds/explosion.wav")
explosion_fx1.set_volume(0.15)

explosion_fx2 = pygame.mixer.Sound("assets/sounds/explosion2.wav")
explosion_fx2.set_volume(0.15)

laser = pygame.mixer.Sound("assets/sounds/laser.wav")
laser.set_volume(0.15)

# Define Colors
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# Define game variables
rows = 5
cols = 5

alien_cooldown = 1000  # bullet cooldown in ms.
last_alien_shot = pygame.time.get_ticks()  # Start timer as soon as the game starts.
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0   # 0 means game starts. 1 means player wins. 2 means player loses.


def draw_bg():
    screen.blit(bg, (0, 0))


# Add text to the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Create sprite group for tracking list of activate sprites
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()


# Create Player
spaceship = Spaceship(screen, SCREEN_WIDTH, SCREEN_HEIGHT, int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT - 100),
                      red, green, 3, bullet_group, alien_group, explosion_group, laser, explosion_fx1,
                      game_over)
spaceship_group.add(spaceship)


def create_aliens():
    for row in range(rows):
        for col in range(cols):
            alien = Aliens(100 + col * 100, 100 + row * 70)
            alien_group.add(alien)


create_aliens()


run = True
while run:
    clock.tick(FPS)

    # Draw assets ...
    draw_bg()

    if countdown == 0:
        # Create Alien bullets at random
        time_now = pygame.time.get_ticks()
        if (time_now - last_alien_shot > alien_cooldown and
                len(alien_bullet_group) < 5) and len(alien_group) > 0:
            attacking_alien = random.choice(alien_group.sprites())
            alien_bullet = AlienBullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom,
                                        SCREEN_HEIGHT, spaceship, spaceship_group, explosion_group, explosion_fx2)
            alien_bullet_group.add(alien_bullet)
            last_alien_shot = time_now

        # Check if all of the aliens have been killed.
        if len(alien_group) == 0:
            game_over = 1

        if game_over == 0:
            # Update spaceship
            game_over = spaceship.update()

            # Update sprite Groups.
            bullet_group.update()
            alien_group.update()
            alien_bullet_group.update()
        else:
            if game_over == 2:
                draw_text("Game Over!", font40, white, int(SCREEN_WIDTH / 2 - 100), int(SCREEN_HEIGHT / 2 + 50))
            elif game_over == 1:
                draw_text("You Win!", font40, white, int(SCREEN_WIDTH / 2 - 100), int(SCREEN_HEIGHT / 2 + 50))

    elif countdown > 0:
        draw_text("Get Ready!", font40, white, int(SCREEN_WIDTH / 2 - 100), int(SCREEN_HEIGHT / 2 + 50))
        draw_text(str(countdown), font40, white, int(SCREEN_WIDTH / 2 - 10), int(SCREEN_HEIGHT / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer

    explosion_group.update()    # Keeping as is so that they do not end prematurely.

    # Draw Sprite Groups
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
    explosion_group.draw(screen)

    # Handle Events ...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
