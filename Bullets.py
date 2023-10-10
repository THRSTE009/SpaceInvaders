import pygame
from Explosion import Explosion


class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, alien_group, explosion_group):
        self.sprite = pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.alien_group = alien_group
        self.explosion_group = explosion_group

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()  # garbage collection for when bullets leave the screen.

        # Collision detection
        if pygame.sprite.spritecollide(self, self.alien_group, dokill=True):
            self.kill()  # ensures bullets destroy themselves upon contact.
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            self.explosion_group.add(explosion)
