import pygame

from Explosion import Explosion


# import Bullets


class AlienBullets(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_height, spaceship, spaceship_group, explosion_group, explosion_fx2):
        # super().__init__( x, y)
        pygame.sprite.Sprite.__init__(self)
        self.screen_height = screen_height
        self.image = pygame.image.load("assets/alien_bullet.png")  # Overriding inherited property.
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.spaceship = spaceship
        self.spaceship_group = spaceship_group
        self.explosion_group = explosion_group
        self.explosion_fx2 = explosion_fx2

    def update(self):
        self.rect.y += 2
        if self.rect.top > self.screen_height:
            self.kill()  # garbage collection for when bullets leave the screen.

        # Collision detection
        if pygame.sprite.spritecollide(self, self.spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            self.spaceship.health_remaining -= 1    # Reduce spaceship health
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            self.explosion_group.add(explosion)
            self.explosion_fx2.play()
