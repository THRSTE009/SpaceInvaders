# Tutorial by Coding With Russ
# https://www.youtube.com/watch?v=mqz1_wRSMwo&ab_channel=CodingWithRuss
# Game created by Steven Theron
# 9 October 2023

import pygame
from pygame.locals import *
import random

from Spaceship import Spaceship
from Aliens import Aliens
from AlienBullets import AlienBullets

# Define fps
clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load Game Assets
bg = pygame.image.load("assets/background1.png")

# Define Colors
red = (255, 0, 0)
green = (0, 255, 0)

# Define game variables
rows = 5
cols = 5

alien_cooldown = 1000  # bullet cooldown in ms.
last_alien_shot = pygame.time.get_ticks()  # Start timer as soon as the game starts.


def draw_bg():
    screen.blit(bg, (0, 0))


# Create sprite group for tracking list of activate sprites
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()


# Create Player
spaceship = Spaceship(screen, SCREEN_WIDTH, SCREEN_HEIGHT, int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT - 100),
                      red, green, 3, bullet_group, alien_group, explosion_group)
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

    # Create Alien bullets at random
    time_now = pygame.time.get_ticks()
    if (time_now - last_alien_shot > alien_cooldown and
            len(alien_bullet_group) < 5) and len(alien_group) > 0:
        attacking_alien = random.choice(alien_group.sprites())
        alien_bullet = AlienBullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom,
                                    SCREEN_HEIGHT, spaceship, spaceship_group, explosion_group)
        alien_bullet_group.add(alien_bullet)
        last_alien_shot = time_now


    # Handle Events ...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update spaceship
    spaceship.update()

    # Update sprite Groups.
    bullet_group.update()
    alien_group.update()
    alien_bullet_group.update()
    explosion_group.update()

    # Draw Sprite Groups
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
    explosion_group.draw(screen)

    pygame.display.update()

pygame.quit()
