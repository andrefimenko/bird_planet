from random import randint

import pygame
from pygame.sprite import Sprite

class CeilingRock(Sprite):

    def __init__(self, bp_game):

        super().__init__()
        self.screen = bp_game.screen
        self.settings = bp_game.settings
        self.ceiling_color = self.settings.stone_color
        # self.stone_color = self.settings.stone_color

        self.rect = pygame.Rect(
            self.screen.get_rect().width,
            self.screen.get_rect().height,
            self.settings.rock_width, 20)

        # self.rect.x = self.screen.get_rect().width
        # self.rect.y = self.screen.get_rect().height
        # self.rect.width = self.settings.rock_width

        self.x = float(self.rect.x)

    def update(self):

        self.x -= self.settings.planet_speed

        self.rect.x = self.x

    def draw_ceiling_rock(self):
        pygame.draw.rect(self.screen, self.ceiling_color, self.rect)