import pygame

from Bullets import Bullets
from Explosion import Explosion


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen, screen_width, screen_height, x, y, red, green, health,
                 bullet_group, alien_group, explosion_group, laser, explosion_fx1, game_over):
        pygame.sprite.Sprite.__init__(self)  # inherit Sprite class within the Spaceship class.
        self.mask = None
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.image = pygame.image.load("assets/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.red = red
        self.green = green

        self.health_start = health
        self.health_remaining = health

        self.bullet_group = bullet_group
        self.last_shot = pygame.time.get_ticks()  # Measures when bullet was created.

        self.alien_group = alien_group
        self.explosion_group = explosion_group

        self.laser = laser
        self.explosion_fx1 = explosion_fx1

        self.game_over = game_over

    def update(self):
        speed = 6
        bullet_cooldown = 500  # milliseconds.

        # Get key pressed
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < self.screen_width:
            self.rect.x += speed

        # Record current time
        time_now = pygame.time.get_ticks()

        # Shoot
        if key[pygame.K_SPACE] and (time_now - self.last_shot > bullet_cooldown):
            bullet = Bullets(self.rect.centerx, self.rect.top,
                             self.alien_group, self.explosion_group,
                             self.explosion_fx1)
            self.bullet_group.add(bullet)
            self.last_shot = time_now
            self.laser.play()

        # Update Mask for perfect pixel collision detection.
        self.mask = pygame.mask.from_surface(self.image)

        # Draw Health bar
        pygame.draw.rect(self.screen, self.red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        # red rect will always be below the green health bar.
        if self.health_remaining > 0:
            pygame.draw.rect(self.screen, self.green, (self.rect.x, (self.rect.bottom + 10),
                                             int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining == 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            self.explosion_group.add(explosion)
            self.kill()
            self.explosion_fx1.play()
            self.game_over = 2

        return self.game_over
