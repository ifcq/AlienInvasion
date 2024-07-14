import random
class Settings:
    """all the settings for AlienInvasion, put here"""
    def __init__(self):
        """initialize the settings class, you can modify it here."""
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        self.fps = 60
        self.caption = 'Alien Invasion'
        self.ship_speed = 7.0
        self.bullet_speed = 7.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (30,30,30)
        self.bullet_max = 3
        self.alien_speed = 5
        self.fleet_drop_speed = 10
        # 1是向右移动，-1是向左移动，到时候直接乘以速度然后赋值给x
        self.fleet_direction = 1
        self.ship_limit = 3
        self.button_width = 200
        self.button_height = 50
        self.button_color = (0, 135, 0)
        self.button_text_color = (255, 255, 255)
        self.alien_points = 10

    def speed_up(self):
        self.alien_speed += 1
        self.bullet_max += 1
        self.fleet_drop_speed += 0.5
        self.ship_speed += 1.5
        self.bullet_speed += 1.5
        self.alien_points += 10

    def reset_speed(self):
        self.alien_speed = 5
        self.bullet_max = 3
        self.fleet_drop_speed = 10
        self.ship_speed = 5.0
        self.bullet_speed = 7.0
        self.alien_points = 10



    def random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

