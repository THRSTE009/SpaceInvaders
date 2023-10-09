import pygame
from pygame.locals import *

# Define fps
clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load Game Assets
bg = pygame.image.load("assets/background.png")

# Define Colors
red = (255, 0, 0)
green = (0, 255, 0)

def draw_bg():
    screen.blit(bg, (0, 0))


# Create spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self) # inherit Sprite class within the Spaceship class.
        self.image = pygame.image.load("assets/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health

    def update(self):
        speed = 6

        # Get key pressed
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += speed

        # Draw Health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        # red rect will always be below the green health bar.
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10),
                                             int(self.rect.width * (self.health_remaining / self.health_start)), 15))


# Create sprite group for tracking list of activate sprites
spaceship_group = pygame.sprite.Group()

# Create Player
spaceship = Spaceship(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT - 100), 3)
spaceship_group.add(spaceship)


run = True
while run:
    clock.tick(FPS)

    # Draw assets ...
    draw_bg()

    # Handle Events ...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update spaceship
    spaceship.update()

    # Draw Sprite Groups
    spaceship_group.draw(screen)

    pygame.display.update()

pygame.quit()