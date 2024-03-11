from random import randint

import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):

    def __init__(self, bp_game):

        super().__init__()
        self.screen = bp_game.screen
        self.settings = bp_game.settings
        self.screen_rect = bp_game.screen.get_rect()

        self.current_ground_level = bp_game.current_ground_level
        self.current_ceiling_level = bp_game.current_ceiling_level

        self.ground_unit_height = bp_game.ground_unit.height

        self.image = pygame.image.load('images/enemy.bmp')
        self.rect = self.image.get_rect()

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):

        screen_rect = self.screen.get_rect()
        print(f"Current ceiling {self.current_ceiling_level}")
        print(f"Self rect top {self.rect.top}")
        return (self.rect.top < 788 - self.current_ceiling_level) or (self.rect.bottom >
                                       screen_rect.bottom
                                       - self.current_ground_level
                                       - self.ground_unit_height)

    def update(self):

        self.x -= self.settings.enemy_hor_speed
        self.rect.x = self.x
        self.y += self.settings.enemy_vert_speed * self.settings.enemy_vert_direction
        self.rect.y = self.y
