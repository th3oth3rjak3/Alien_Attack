"""This module is to store game statistics such as high scores and ship collisions."""
class GameStats:
    """Track game statistics for Alien Invasions."""
    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        self.game_paused = False
        #Current high score should be reset when the game is closed.
        self.current_high_score = 0
        self.best_level = 1

    def reset_stats(self):
        """Initialize statstics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
