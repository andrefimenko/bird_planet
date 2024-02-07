import sys
import time

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from star import Star

class BirdPlanet:

    def __init__(self):

        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Bird Planet")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self.star_quantity = (self.screen.get_rect().width *
                         self.screen.get_rect().height) // 10000
        self.current_star_quantity = 0
        self._create_star_sky()

        # self.start_time = time.time()
        self.last_shot_time = 0

    def run_game(self):

        while True:
            self._update_stars()
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            if event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):

        if time.time() - self.last_shot_time > self.settings.gun_fire_rate:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

            self.last_shot_time = time.time()

    def _update_bullets(self):

        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen.get_rect().right:
                self.bullets.remove(bullet)
        # print(len(self.bullets))

    def _update_stars(self):

        if self.star_quantity > self.current_star_quantity:
            self._refill_star_sky()

        self.stars.update()

        for star in self.stars.copy():
            if star.rect.right <= 0: # self.screen.get_rect().right:
                self.stars.remove(star)
                self.current_star_quantity -= 1

    def _create_star_sky(self):

        while self.current_star_quantity < self.star_quantity:
            new_star = Star(self)
            self.stars.add(new_star)
            self.current_star_quantity += 1

    def _refill_star_sky(self):

        while self.current_star_quantity < self.star_quantity:
            new_star = Star(self)
            new_star.x = self.screen.get_rect().width
            self.stars.add(new_star)
            self.current_star_quantity += 1
            print(self.current_star_quantity)

    # def _star_rebirth(self):
    #
    #     if self.star_quantity

    def _update_screen(self):

        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()


        pygame.display.flip()

if __name__ == '__main__':

    bp = BirdPlanet()
    bp.run_game()
