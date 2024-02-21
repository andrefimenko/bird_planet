from random import randint

import pygame
from pygame.sprite import Sprite


class Enemy(Sprite):

    def __init__(self, bp_game):

        super().__init__()
        self.screen = bp_game.screen
        self.settings = bp_game.settings
        self.screen_rect = bp_game.screen.get_rect()

        self.image = pygame.image.load('images/enemy.bmp')
        self.rect = self.image.get_rect()

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):

        self.x -= self.settings.enemy_speed
        self.rect.x = self.x
