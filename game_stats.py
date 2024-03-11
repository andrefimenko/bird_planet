class GameStats:

    def __init__(self, bp_game):

        self.settings = bp_game.settings
        self.reset_stats()

    def reset_stats(self):

        self.ships_left = self.settings.ship_limit
