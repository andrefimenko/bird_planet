import sys
import time
from time import sleep
from random import randint

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from star import Star
from ground import GroundRock
from ceiling import CeilingRock
from scenario import Scenario
from enemy import Enemy
from bird import Bird
from ground_unit import GroundUnit
from ground_bullet import GroundBullet


class BirdPlanet:

    def __init__(self):

        pygame.init()
        self.clock = pygame.time.Clock()
        self.current_time = time.time()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Bird Planet")

        self.stats = GameStats(self)

        self.scenario = Scenario(self)
        self.stage_progress = 0
        self.ceiling_rock = CeilingRock(self)
        self.current_ground_level = 0
        self.current_ceiling_level = 788
        # self.ceiling = True
        # self.current_ceiling_level = self.screen.get_height() + self.ceiling_rock.rect.height
        self.current_ceiling_rock_quantity = 0

        self.ship = Ship(self)
        self.ground_unit = GroundUnit(self)
        self.bullets = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.ground_rocks = pygame.sprite.Group()
        self.ceiling_rocks = pygame.sprite.Group()
        self.birds = pygame.sprite.Group()
        self.ground_units = pygame.sprite.Group()
        self.ground_bullets = pygame.sprite.Group()

        self.star_quantity = (self.screen.get_rect().width
                              * self.screen.get_rect().height) // 10000
        self.current_star_quantity = 0
        self._create_star_sky()

        # self.current_time = current_time.current_time()
        self.last_shot_time = 0

        self.current_enemy_quantity = 0
        self.current_bird_quantity = 0
        self.current_ground_unit_quantity = 0

        self.game_active = True

    def run_game(self):

        while True:
            self.scenario.stages(self.current_time)
            self._update_stars()
            self._check_events()

            if self.game_active:
                self._update_enemies(self.scenario.stage)
                self._update_ground_units()
                self._update_birds(self.scenario.stage)
                self._update_rocks(self.scenario.stage)
                self.ship.update()
                self._update_bullets()
                self._update_ground_bullets()

            print(self.settings.enemy_vert_direction)
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

        # self._fire_ground_bullet()

    def _check_keyup_events(self, event):

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _ship_hit(self):

        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            self.bullets.empty()
            self.enemies.empty()
            self.ground_rocks.empty()
            self.ceiling_rocks.empty()
            self.birds.empty()
            self.stars.empty()
            self.ground_units.empty()
            self.current_ground_level = 0
            self.current_ceiling_level = self.screen_height
            self.current_star_quantity = 0
            self._create_star_sky()
            self.settings.bg_color = (0, 0, 0)
            self.stage_progress = 0

            sleep(0.5)

        else:
            self.game_active = False

    def _fire_bullet(self):

        if time.time() - self.last_shot_time > self.settings.gun_fire_rate:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

            self.last_shot_time = time.time()

    def _fire_ground_bullet(self):

        fire_probability = randint(0, 50)
        if fire_probability == 0:
            new_ground_bullet = GroundBullet(self)
            new_ground_bullet.rect.x = 400
            self.ground_bullets.add(new_ground_bullet)
        # print(f"Ground bullets {len(self.ground_bullets)}")

    def _update_bullets(self):

        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen.get_rect().right:
                self.bullets.remove(bullet)

        self._check_bullet_enemy_collisions()
        self._check_bullet_ground_unit_collisions()
        self._check_bullet_bird_collisions()
        # self._check_ship_enemy_collisions()

    def _check_bullet_enemy_collisions(self):
        collisions_bullet_enemy = pygame.sprite.groupcollide(
            self.bullets, self.enemies, True, True)

    def _check_bullet_ground_unit_collisions(self):
        collisions_bullet_ground_unit = pygame.sprite.groupcollide(
            self.bullets, self.ground_units, True, True)

    def _check_bullet_bird_collisions(self):
        collisions_bullet_bird = pygame.sprite.groupcollide(
            self.bullets, self.birds, True, True)

    # def _check_ship_enemy_collisions(self):
    #     collisions_ship_enemy = pygame.sprite.groupcollide(
    #         self.ship, self.enemies, True, True)

        pygame.sprite.groupcollide(self.bullets, self.ground_rocks, True, False)
        pygame.sprite.groupcollide(self.bullets, self.ceiling_rocks, True, False)

    def _update_ground_bullets(self):

        self.ground_bullets.update()

        for ground_bullet in self.ground_bullets.copy():
            if ground_bullet.rect.left <= 0:
                self.ground_bullets.remove(ground_bullet)

    def _update_stars(self):

        if self.star_quantity > self.current_star_quantity:
            self._refill_star_sky()

        self.stars.update()

        for star in self.stars.copy():
            if star.rect.right <= 0:  # self.screen.get_rect().right:
                self.stars.remove(star)
                self.current_star_quantity -= 1

    def _check_enemies_edges(self):

        for enemy in self.enemies.sprites():
            if enemy.check_edges():
                self._change_enemies_direction()
                break

    def _change_enemies_direction(self):

        for enemy in self.enemies.sprites():
            enemy.rect.y += self.settings.enemy_vert_speed
        self.settings.enemy_vert_direction *= -1

    def _update_enemies(self, stage):

        if 0 <= stage <= 3:
            self._check_enemies_edges()
            enemy_probability = randint(0, 400)
            if enemy_probability == 0:
                new_enemy = Enemy(self)
                new_enemy.x = self.screen.get_rect().width
                new_enemy.y = randint(100, 200)
                new_enemy.rect.y =\
                    randint(0,
                            self.screen_height - int(self.current_ground_level) -
                            self.ground_unit.rect.height * 3)
                self.enemies.add(new_enemy)
                self.current_enemy_quantity += 1

        self.enemies.update()

        if pygame.sprite.spritecollideany(self.ship, self.enemies):
            self._ship_hit()

        for enemy in self.enemies.copy():
            if enemy.rect.right <= 0:
                self.enemies.remove(enemy)

    def _update_birds(self, stage):

        if stage == 1 or stage == 2:
            bird_probability = randint(0, 400)
            if bird_probability == 0:
                new_bird = Bird(self)
                new_bird.x = self.screen.get_rect().width
                new_bird.rect.y =\
                    randint(0,
                            self.screen_height - int(self.current_ground_level) -
                            self.ground_unit.rect.height * 3)
                self.birds.add(new_bird)
                self.current_bird_quantity += 1

        self.birds.update()

        if pygame.sprite.spritecollideany(self.ship, self.birds):
            self._ship_hit()

        for bird in self.birds.copy():
            if bird.rect.right <= 0:
                self.birds.remove(bird)

    def _update_rocks(self, stage):

        self.build_terrain(stage)
        self.ground_rocks.update()
        self.ceiling_rocks.update()
        if pygame.sprite.spritecollideany(self.ship, self.ground_rocks):
            self._ship_hit()

        for g_rock in self.ground_rocks.copy():
            if g_rock.rect.right <= 0:  # self.screen.get_rect().right:
                self.ground_rocks.remove(g_rock)
        for c_rock in self.ceiling_rocks.copy():
            if c_rock.rect.right <= 0:
                self.ceiling_rocks.remove(c_rock)

    def _create_star_sky(self):

        while self.current_star_quantity < self.star_quantity:
            new_star = Star(self)
            self.stars.add(new_star)
            self.current_star_quantity += 1

    def _refill_star_sky(self):

        if self.current_star_quantity < self.star_quantity and self.scenario.stage <= 1:
            new_star = Star(self)
            new_star.x = self.screen.get_rect().width
            self.stars.add(new_star)
            self.current_star_quantity += 1
            print("REfil")
    def build_terrain(self, stage):

        if stage == 1:
            new_rock = GroundRock(self)
            if self.current_ground_level < (self.screen_height * 0.05):
                self.current_ground_level += (randint(
                    int(self.screen_height * -0.05), int(self.screen_height * 0.06))
                                              / randint(10, 15))  # * randint(-1, 2)
            elif self.current_ground_level > (self.screen_height * 0.1):
                self.current_ground_level += (randint(
                    int(self.screen_height * -0.055), int(self.screen_height * 0.055))
                                              / randint(10, 15))
            else:
                self.current_ground_level += (randint(
                    int(self.screen_height * -0.06), int(self.screen_height * 0.05))
                                              / randint(10, 15))
            new_rock.rect.y -= self.current_ground_level
            # new_rock.rect.height = 10
            self.ground_rocks.add(new_rock)

        elif stage == 2:
            new_rock = GroundRock(self)

            if self.current_ground_level <= (self.screen_height * 0.7):
                self.current_ground_level += (randint(
                    int(self.screen_height * -0.05), int(self.screen_height * 0.065))
                                              / randint(10, 15))
                new_rock.rect.y -= self.current_ground_level
            self.ground_rocks.add(new_rock)

        elif stage == 3:
            new_ceiling_stone = CeilingRock(self)

            self.current_ceiling_level -= (randint(
                    int(self.screen_height * -0.05), int(self.screen_height * 0.055))
                                                  / randint(10, 15))

            new_ceiling_stone.rect.y -= self.current_ceiling_level
            self.ceiling_rocks.add(new_ceiling_stone)

            new_ground_stone = GroundRock(self)

            if self.current_ground_level > self.screen_height * 0.1:
                self.current_ground_level += (randint(
                        int(self.screen_height * -0.065), int(self.screen_height * 0.05))
                                                  / randint(10, 15))
            elif self.current_ground_level <= (self.screen_height * 0.1):
                self.current_ground_level += (randint(
                    int(self.screen_height * -0.055), int(self.screen_height * 0.055))
                                              / randint(10, 15))
            else:
                self.current_ground_level += (randint(
                    int(self.screen_height * -0.05), int(self.screen_height * 0.065))
                                              / randint(10, 15))
            new_ground_stone.rect.y -= self.current_ground_level
            self.ground_rocks.add(new_ground_stone)



    def _update_ground_units(self):

        if self.current_ground_level >= 5:
            ground_unit_probability = randint(0, 200)
            if ground_unit_probability == 0:
                new_ground_unit = GroundUnit(self)
                new_ground_unit.x = self.screen.get_rect().width
                new_ground_unit.rect.y -= self.current_ground_level
                # print(f"Update ground unit. Current ground level: {self.current_ground_level}")
                self.ground_units.add(new_ground_unit)
                # self.current_ground_unit_quantity += 1

        self._fire_ground_bullet()
        self.ground_units.update()

        for unit in self.ground_units.copy():
            if unit.rect.right <= 0:
                self.ground_units.remove(unit)

    def _update_screen(self):

        if self.scenario.stage == 0:
            self.stage_progress = ((time.time() - self.scenario.scenario['start_time'])
                                   / self.scenario.scenario['de_orbiting_time'])
            self.settings.bg_color = 'black' # (
                # int(120 * self.stage_progress),
                # int(188 * self.stage_progress),
                # int(235 * self.stage_progress))

        elif self.scenario.stage == 1:
            self.settings.bg_color = 'black' # '(120, 188, 235)

        elif (self.scenario.stage == 2 and self.current_ceiling_rock_quantity
              > (self.screen_width / self.settings.rock_width)):
            self.settings.bg_color = (
                int(self.settings.bg_color[0] / 1.01),
                int(self.settings.bg_color[1] / 1.01),
                int(self.settings.bg_color[2] / 1.01))

        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        self.enemies.draw(self.screen)
        self.birds.draw(self.screen)
        self.ground_units.draw(self.screen)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        for ground_bullet in self.ground_bullets.sprites():
            ground_bullet.draw_ground_bullet()

        for ground_rock in self.ground_rocks.sprites():
            ground_rock.draw_ground_rock()
        for ceiling_rock in self.ceiling_rocks.sprites():
            ceiling_rock.draw_ceiling_rock()

        self.ship.blitme()
        # self.ground_unit.blitme()

        pygame.display.flip()


if __name__ == '__main__':
    bp = BirdPlanet()
    bp.run_game()
