
import pygame
import random


class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/aliens/alien" + str(random.randint(1, 5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        # Movements
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1  # move to the other side.
            self.move_counter *= self.move_direction
