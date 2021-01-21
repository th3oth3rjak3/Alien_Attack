"""A module to create a scoreboard for Alien Invasion."""
import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        self.current_border_rect = pygame.Rect(0, 0, 360, 110)
        self.current_border_rect.center = self.screen_rect.center
        self.current_border_rect.top = 25
        self.current_score_rect = pygame.Rect(0, 0, 350, 100)
        self.current_score_rect.center = self.current_border_rect.center

        self.player_score_rect = pygame.Rect(0, 0, 250, 100)
        self.border_rect = pygame.Rect(0, 0, 260, 110)
        self.border_rect.top = 25
        self.border_rect.right = self.screen_rect.right - 25
        self.player_score_rect.center = self.border_rect.center

        #Font settings for scoring information.
        self.text_color = ai_game.settings.font_color
        self.font = pygame.font.SysFont(None, 48)

        #Prepare the initial score image.
        self.prep_score()
        self.prep_current_high_score()
        self.prep_level()
        self.prep_best_level()
        self.prep_ships()

    def prep_score(self):
        """Turn score into a rendered image."""
        score_str = (f"Score: {self.format_score(self.stats.score)}")
        self.score_image = self.font.render(score_str, True, self.text_color, None)

        #Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.center = self.player_score_rect.center
        self.score_rect.top = self.player_score_rect.top + 15

    def prep_current_high_score(self):
        """Turn current high score into a rendered image."""
        current_high_score = self.stats.current_high_score
        current_high_score_str = (f"Best Score: {self.format_score(current_high_score)}")
        self.current_high_score_image = self.font.render(current_high_score_str,True, self.text_color, None)

        #Center the current high score at the top of the screen.
        self.current_high_score_rect = self.current_high_score_image.get_rect()
        self.current_high_score_rect.center = self.current_score_rect.center
        self.current_high_score_rect.top = self.current_score_rect.top + 15

    def prep_level(self):
        """Turn the level into a rendered image to display on screen."""
        level_str = (f"Level: {self.stats.level}")
        self.level_image = self.font.render(level_str, True, self.text_color, None)

        #Put the level image beneath the current score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.center = self.score_rect.center
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_best_level(self):
        """Turn the best level reached into a rendered image."""
        best_level_str = (f"Best Level: {self.stats.best_level}")
        self.best_level_image = self.font.render(best_level_str, True, self.text_color, None)

        #Put the best level image beneath the best score.
        self.best_level_rect = self.best_level_image.get_rect()
        self.best_level_rect.center = self.screen_rect.center
        self.best_level_rect.top = self.current_high_score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 25 + ship_number * ship.rect.width
            ship.rect.y = 25
            self.ships.add(ship)

    def show_score(self):
        """Draw score, ships remaining, and level to the screen."""
        self.screen.fill(self.ai_game.play_button.border_color, self.current_border_rect)
        self.screen.fill(self.ai_game.play_button.button_color, self.current_score_rect)
        self.screen.fill(self.ai_game.play_button.border_color, self.border_rect)
        self.screen.fill(self.ai_game.play_button.button_color, self.player_score_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.current_high_score_image, self.current_high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.best_level_image, self.best_level_rect)
        self.ships.draw(self.screen)

    def format_score(self, input_object):
        """Formats the score for use in the Alien Invasion game."""
        score_str = str(f"{input_object:,}")
        return score_str

    def check_current_high_score(self):
        """Check to see if there is a new high score."""
        if self.stats.score > self.stats.current_high_score:
            self.stats.current_high_score = self.stats.score
            self.prep_current_high_score()

    def check_best_level(self):
        """Check to see if there is a new highest level."""
        if self.stats.level > self.stats.best_level:
            self.stats.best_level = self.stats.level
            self.prep_best_level()
