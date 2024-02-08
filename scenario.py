import time

from rock import Rock


class Scenario:

    def __init__(self, bp_game):

        self.screen = bp_game.screen
        self.settings = bp_game.settings

        self.stage = 0

        self.start_time = time.time()
        self.de_orbiting_time = 2 # 120
        self.above_the_surface_time = 120
        self.in_the_cave_time = 2 # 120
        self.final_battle_hp = 10

    def stages(self, current_time):
        """0 - De-orbiting; 1 - Above the surface; 2 - In the cave; 3 - Final battle"""

        if time.time() > self.de_orbiting_time + self.above_the_surface_time + self.in_the_cave_time + current_time:
            self.stage = 3
        elif time.time() > self.de_orbiting_time + self.above_the_surface_time + current_time:
            self.stage = 2
        elif time.time() > self.de_orbiting_time + current_time:
            self.stage = 1
        else:
            self.stage = 0

    def _build_terrain(self, stage):

        if stage == 1:
            new_rock = Rock(self)
            new_rock.x = self.screen.get_rect().width


    def _final_battle(self):
        print("Fin")
