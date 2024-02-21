from random import randint

import pygame
from pygame.sprite import Sprite


class GroundUnit(Sprite):

    def __init__(self, bp_game):

        super().__init__()
        self.screen = bp_game.screen
        self.settings = bp_game.settings
        self.screen_rect = bp_game.screen.get_rect()

        self.image = pygame.image.load('images/ground_unit.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.screen.get_rect().width
        self.rect.y = self.screen.get_rect().height - self.rect.height * 0.75

        self.x = float(self.rect.x)
        # self.y = float(self.rect.y)

    def update(self):

        self.x -= self.settings.planet_speed
        self.rect.x = self.x

    # def blitme(self):
    #
    #     self.screen.blit(self.image, self.rect)
