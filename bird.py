from random import randint

import pygame
from pygame.sprite import Sprite

class Bird(Sprite):

    def __init__(self, bp_game):

        super().__init__()
        self.screen = bp_game.screen
        self.settings = bp_game.settings

        self.image = pygame.image.load('images/bird.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.screen.get_rect().width
        self.rect.y = randint(0, self.screen.get_rect().height - 100)

        self.x = float(self.rect.x)

    def update(self):

        self.x -= self.settings.bird_speed
        self.rect.x = self.x
