from random import random, randint

import pygame
from pygame.sprite import Sprite

class Star(Sprite):

    def __init__(self, bp_game):

        super().__init__()
        self.screen = bp_game.screen

        self.image = pygame.image.load('images/1453737154.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = randint(0, bp_game.screen.get_rect().width)
        self.rect.y = randint(0, bp_game.screen.get_rect().height)

        # print(bp_game.screen.get_rect().width)

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
