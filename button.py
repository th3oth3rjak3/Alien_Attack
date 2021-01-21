"""Creating a button module for Alien Invasion"""
import pygame.font
from settings import Settings

class Button:
    """A button class to create a play button for Alien Invasion."""

    def __init__(self, ai_game, msg, left_pos = None, right_pos = None, top_pos = None, bottom_pos = None, center_pos = None):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = Settings()

        #Set the dimensions and properties of the button.
        self.width, self.height = 250, 50
        self.bg_width, self.bg_height = 260, 60
        self.button_color = (27, 145, 171)
        self.border_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        #Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.bg_rect = pygame.Rect(0, 0, self.bg_width, self.bg_height)
        if left_pos:
            self.rect.left = left_pos
            self.bg_rect.center = self.rect.center
        if right_pos:
            self.rect.right = right_pos
            self.bg_rect.center = self.rect.center
        if top_pos:
            self.rect.top = top_pos
            self.bg_rect.center = self.rect.center
        if bottom_pos:
            self.rect.bottom = bottom_pos
            self.bg_rect.center = self.rect.center
        if center_pos:
            self.rect.center = self.screen_rect.center
            self.bg_rect.center = self.screen_rect.center

        #The button message only needs to be prepped once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.settings.button_font_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.border_color, self.bg_rect)
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
