"""A module to store all the settings for Alien Invasion."""
import ctypes
import pygame


class Settings:
    """A class to store all the settings for Alien Invasion."""
    def __init__(self):
        """Initializes game static settings."""
        #Screen settings:
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [self.screen_width, self.screen_height] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        #self.screen_width = 1200
        #self.screen_height = 800
        self.bg_color = (130, 131, 131)
        self.bg = pygame.image.load(r"images/galaxy.png")
        self.font_color = (0, 0, 0)
        self.button_font_color = (0, 0, 0)

        #Ship settings:
        self.ship_limit = 2
        self.ship_max_speed = 3.0 * 5

        #Bullet settings:
        self.bullet_width = 4
        self.bullet_height = 20
        self.bullet_color = (255, 206, 4)
        self.bullets_allowed = 5
        self.bullet_max_speed = 6.0 * 5
        self.max_bullet_cooldown = 250

        #Alien settings:
        self.fleet_drop_speed = 10

        #How quickly the game speeds up.
        self.speedup_scale = 1.025
        self.cooldown_scale = 1.025
        self.score_scale = 1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize all the dynamic settings."""
        self.ship_speed = 1.5 * 5
        self.bullet_speed = 2.0 * 5
        self.alien_speed = 0.5 * 5
        self.bullet_cooldown = 125
        self.alien_points = 1

        #fleet_direction of 1 represents right, -1 represents left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings."""
        if self.ship_speed * self.speedup_scale > self.ship_max_speed:
            self.ship_speed = self.ship_max_speed
        else:
            self.ship_speed *= self.speedup_scale
        if self.bullet_speed * self.speedup_scale > self.ship_max_speed:
            self.bullet_speed = self.bullet_max_speed
        else:
            self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        if self.bullet_cooldown * self.cooldown_scale > self.max_bullet_cooldown:
            self.bullet_cooldown = self.max_bullet_cooldown
        else:
            self.bullet_cooldown *= self.cooldown_scale
        self.alien_points += self.score_scale
