class Settings:

    def __init__(self):

        # Screen settings
        self.bg_color = (0, 0, 0)

        # Star settings
        self.star_speed = 0.8

        # Enemy settings
        self.enemy_speed = 2

        # Ship settings
        self.ship_vert_speed = 1.5
        self.ship_hor_speed = 3

        # Planet settings
        self.planet_speed = 1.6

        # Bullet settings
        self.bullet_speed = 6
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = "white"
        self.gun_fire_rate = 1

        # Ground bullet settings
        self.ground_bullet_vert_speed = 6
        self.ground_bullet_hor_speed = 3 # self.planet_speed + 2
        self.ground_bullet_width = 3
        self.ground_bullet_height = 15
        self.ground_bullet_color = 'red'

        # Ground settings
        self.ground_color = "green"

        self.rock_width = 2

        # Cave ceiling settings
        self.stone_color = "red"

        # Bird settings
        self.bird_speed = 2
