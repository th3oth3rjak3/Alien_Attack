"""A module to manage the ship class."""
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""
    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #load the ship image and get its rect
        self.image = pygame.image.load(r"images\small_space_ship.png")
        self.rect = self.image.get_rect()

        #Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        #Store a decimal value for the ship's horizontal position.
        self.x_position = float(self.rect.x)

        #Movement Flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on movement flags."""
        #Update the ship's value not the rect position.
        if self.moving_right and self.rect.right + self.settings.ship_speed < self.screen_rect.right:
            self.x_position += self.settings.ship_speed
        elif self.moving_right and self.rect.right + self.settings.ship_speed >= self.screen_rect.right:
            self.x_position = self.screen_rect.right - self.rect.width
        if self.moving_left and self.rect.left - self.settings.ship_speed > self.screen_rect.left:
            self.x_position -= self.settings.ship_speed
        elif self.moving_left and self.rect.left - self.settings.ship_speed <= self.screen_rect.left:
            self.x_position = self.screen_rect.left

        #Finally, update the rect position based on the x position.
        self.rect.x = self.x_position

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x_position = float(self.rect.x)
