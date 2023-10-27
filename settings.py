import pygame
class Settings():

    def __init__(self):

        self.screen_width = 1200
        self.screen_height = 800
        self.background_image = pygame.image.load('images/background.jpg')




        self.bullet_width = 4
        self.bullet_height = 25
        self.bullet_color = 0, 0, 255
        self.allowed = 3
        self.ship_limit = 3
        self.alien_drop = 30
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 2
        self.bullet_speed = 3
        self.alien_speed = 1
        self.fleet_direction = 1
        self.alien_points = 10

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

