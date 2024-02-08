from random import randint

import pygame
from pygame.sprite import Sprite

class Bird(Sprite):

    def __init__(self, bp_game):

        super().__init__()
        self.screen = bp_game.screen

        self.image = pygame.image.load('images/bird.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = randint(0, self.screen.get_rect().height)
