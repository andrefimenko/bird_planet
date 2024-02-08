from random import randint

import pygame
from pygame.sprite import Sprite

class Rock(Sprite):

    def __init__(self, bp_game):

        super().__init__()
        self.screen = bp_game.screen
        self.settings = bp_game.settings
        self.ground_color = self.settings.ground_color
        self.ceiling_color = self.settings.ceiling_color

        self.rect = pygame.Rect(0, 0, self.settings.rock_width, 0)

        self.rect.x = self.screen.get_rect().width
        # self.rect.y = 500

        self.x = float(self.rect.x)

    def update(self):

        self.x -= self.settings.planet_speed

        self.rect.x = self.x


    def draw_rock(self):

        pygame.draw.rect(self.screen, self.ground_color, self.rect)