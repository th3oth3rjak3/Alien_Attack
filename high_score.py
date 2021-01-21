"""This module reads and writes high scores to a JSON file."""
from operator import itemgetter
import json
import pygame

from settings import Settings

class HighScore:
    """This class manages the high score reading and writing to file logic."""

    def __init__(self, ai_game):
        """Initialize screen area and high score functions."""
        self.settings = Settings()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        pygame.key.set_repeat(500, 100)
        self.stats = ai_game.stats
        self.input_rect_size = self.screen_rect.center
        self.input_rect_width = 400
        self.input_rect_height = 48
        self.input_rect = pygame.Rect(self.input_rect_size[0] - (self.input_rect_width / 2), self.input_rect_size[1] - (self.input_rect_height / 2), self.input_rect_width, self.input_rect_height)
        self.input_rect_center = pygame.Rect(self.input_rect_size[0] - (self.input_rect_width / 2), self.input_rect_size[1] - (self.input_rect_height / 2), self.input_rect_width, self.input_rect_height)
        self.font = pygame.font.SysFont(None, 48)
        self.banner_font = pygame.font.SysFont(None, 72)
        self.message_text = "What's your name, winner?"
        self.message_image = self.font.render(self.message_text, True, self.settings.font_color, None)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.screen_rect.center
        self.message_image_rect.top -= 50
        self.banner_text = "New High Score!"
        self.banner_text_image = self.banner_font.render(self.banner_text, True, self.settings.font_color, None)
        self.banner_text_rect = self.banner_text_image.get_rect()
        self.banner_text_rect.center = self.screen_rect.center
        self.banner_text_rect.bottom = self.message_image_rect.top - 25
        self.user_name = ""
        self.entering_name = False

    def check_high_score(self, new_score, high_scores):
        """Checks to see if the new score can go on the high score list."""
        for high_score in high_scores:
            if new_score > high_score["Score"]:
                return True
        return False

    def add_high_score(self, user_name, level, new_score, high_scores):
        """Adds a high score to the list of scores and returns the new list to write to file."""
        high_scores.append({"Name": user_name, "Level": level, "Score": new_score})
        high_scores.sort(key=itemgetter("Score"), reverse=True)
        while len(high_scores) > 5:
            high_scores.pop()
        return high_scores

    def read_from_file(self, file_name):
        """Reads high scores from the file and returns the list of dictionaries."""
        with open(file_name) as f:
            high_scores = json.load(f)
        return high_scores

    def write_to_file(self, file_name, high_scores):
        """Writes the list of high score dictionaries to file using JSON."""
        with open(file_name, "w") as f:
            json.dump(high_scores,f)

    def show_input_screen(self):
        """Shows the high score user name input screen and returns the user's name."""
        self.entering_name = True
        self.user_name = ""
        while self.entering_name:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_name = self.user_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.entering_name = False
                    else:
                        if len(self.user_name) < 20:
                            self.user_name += event.unicode
            self.text_image = self.font.render(self.user_name, True, self.settings.font_color, None)
            self.text_rect = self.text_image.get_rect()
            self.text_rect.center = self.screen_rect.center
            screen_bg_image = self.settings.bg
            screen_bg_rect = screen_bg_image.get_rect()
            screen_bg_rect.center = self.screen.get_rect().center
            bg_box_border = pygame.Rect(0, 0, 500, 250)
            bg_box_border.center = self.screen_rect.center
            bg_box_border.top -= 50
            bg_box_center = pygame.Rect(0, 0, 490, 240)
            bg_box_center.center = bg_box_border.center
            self.screen.blit(screen_bg_image, screen_bg_rect)
            self.screen.fill(self.ai_game.play_button.border_color, bg_box_border)
            self.screen.fill(self.ai_game.play_button.button_color, bg_box_center)
            self.ai_game.sb.show_score()
            pygame.draw.rect(self.screen, (12, 115, 138), self.input_rect_center)
            pygame.draw.rect(self.screen, self.ai_game.play_button.border_color, self.input_rect, 2)
            
            self.screen.blit(self.text_image, self.text_rect)
            self.screen.blit(self.message_image, self.message_image_rect)
            self.screen.blit(self.banner_text_image, self.banner_text_rect)
            pygame.display.flip()
        return self.user_name

    def reset_high_scores(self):
        """Resets the high scores back to factory default settings."""
        file_name = "high_scores.json"
        default_high_scores = [{"Name": "(empty)", "Level": 0, "Score": 0}, {"Name": "(empty)", "Level": 0, "Score": 0}, {"Name": "(empty)", "Level": 0, "Score": 0}, {"Name": "(empty)", "Level": 0, "Score": 0}, {"Name": "(empty)", "Level": 0, "Score": 0}]
        self.write_to_file(file_name, default_high_scores)
