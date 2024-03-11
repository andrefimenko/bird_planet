import pygame
from pygame.sprite import Sprite

class GroundBullet(Sprite):

    def __init__(self, bp_game):

        super().__init__()
        self.screen = bp_game.screen
        self.settings = bp_game.settings
        self.color = 'white'

        self.rect = pygame.Rect(bp_game.ground_unit.rect.x,
                                bp_game.ground_unit.rect.y
                                , self.settings.ground_bullet_width,
                                self.settings.ground_bullet_height)
        # self.rect.midbottom = bp_game.ground_unit.rect.midtop

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):

        self.x -= self.settings.ground_bullet_hor_speed
        self.y -= self.settings.ground_bullet_vert_speed

        self.rect.x = self.x
        self.rect.y = self.y

    def draw_ground_bullet(self):

        pygame.draw.rect(self.screen, self.color, self.rect)
