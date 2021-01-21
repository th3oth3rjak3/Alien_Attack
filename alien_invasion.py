"""The main body of the Alien Invasion game!"""
import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullets import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from high_score import HighScore

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    #Button modifications:

    #Score modifications:
    #TODO: Reduce number of points per alien when weapon enhancements are added.

    #Screen modifications:
    #TODO: Make an instructions page that explains what keys to use.
    #TODO: Make a welcome screen with the title and created by information that displays for some amount of time before the play/instruction buttons show up. Put Play, Instructions, High Score, and Quit buttons on this page.
    #TODO: Make a level up screen.

    #Event Modifications:

    #Game Enhancements:
    #TODO: Come up with weapon enhancements at level increments of 5?
    #TODO: Randomly drop a shield after some number of aliens are shot down. Shield only lasts for a set amount of time and takes 1 bullet.
    #TODO: At some level, get a second buddy ship.
    #TODO: At some level, aliens shoot back.

    def __init__(self):
        """Initialize the game and create game resources."""
        icon = pygame.image.load(r"images/small_space_ship.png")
        pygame.display.set_icon(icon)
        pygame.init()
        self.settings = Settings()
        #Use theses settings for partial screen mode:
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        #Use these settings for fullscreen mode:
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Attack")
        #Create an instance to store game statistics.
        self.stats = GameStats(self)
        self.settings.initialize_dynamic_settings()
        self.high_score = HighScore(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.bullets.firing_bullets = False
        self.previous_bullet_time = pygame.time.get_ticks()
        self.current_bullet_time = pygame.time.get_ticks()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.pause_button = Button(self, "Paused (P)", center_pos = True)
        self.play_button = Button(self, "Play (P)", bottom_pos = (self.settings.screen_height / 2 + 100), left_pos = (self.settings.screen_width / 2) - (self.pause_button.width / 2))
        self.instructions_button = Button(self, "Instructions (I)", top_pos = self.play_button.rect.bottom + 20, left_pos = (self.settings.screen_width / 2) - (self.pause_button.width / 2))
        self.high_score_button = Button(self, "High Scores (H)", top_pos = self.instructions_button.rect.bottom + 20, left_pos = self.instructions_button.rect.left)
        self.quit_button = Button(self, "Quit (Q)", top_pos = self.high_score_button.rect.bottom + 20, left_pos = self.high_score_button.rect.left)
        self.back_button = Button(self, "Back (B)", bottom_pos = self.screen.get_rect().bottom - 100, left_pos = self.quit_button.rect.left)
        self.reset_scores_button = Button(self, "Reset (R)", bottom_pos = self.back_button.rect.top - 20, left_pos = self.back_button.rect.left)
        self.sb = Scoreboard(self)
        self.showing_instructions = False
        self.viewing_high_scores = False
        self.hs_banner_text = "Top 5 High Scores"
        self.banner_font = pygame.font.SysFont(None, 72)
        self.hs_banner_text_image = self.banner_font.render(self.hs_banner_text, True, self.settings.font_color, None)
        self.hs_banner_text_rect = self.hs_banner_text_image.get_rect()
        self.hs_banner_text_rect.center = self.screen.get_rect().center
        self.hs_banner_text_rect.top = 50
        self.font = pygame.font.SysFont(None, 48)
        self.ul_font = pygame.font.SysFont(None, 48, bold=True)
        self.clock = pygame.time.Clock()

    def _check_events(self):
        """Responds to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.stats.game_active:
                    self._check_pause_button(mouse_pos)
                else:
                    self._check_play_button(mouse_pos)
                    self._check_instructions_button(mouse_pos)
                    self._check_high_score_button(mouse_pos)
                    self._check_quit_button(mouse_pos)
                if self.showing_instructions or self.viewing_high_scores:
                    self._check_back_button(mouse_pos)
                if self.viewing_high_scores:
                    self._check_reset_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit(0)
        elif event.key == pygame.K_SPACE:
            self.bullets.firing_bullets = True

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_SPACE:
            self.bullets.firing_bullets = False
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self.prep_game()
            elif self.stats.game_active:
                self.stats.game_paused = not self.stats.game_paused
            if self.stats.game_paused:
                self._update_screen()
                pygame.mouse.set_visible(True)
            else:
                pygame.mouse.set_visible(False)
        elif event.key == pygame.K_h:
            if not self.stats.game_active:
                self.viewing_high_scores = True
        elif event.key == pygame.K_i:
            if not self.stats.game_active:
                self.showing_instructions = True
        elif event.key == pygame.K_b:
            if not self.stats.game_active:
                if self.showing_instructions:
                    self.showing_instructions = False
                if self.viewing_high_scores:
                    self.viewing_high_scores = False
        elif event.key == pygame.K_r:
            if not self.stats.game_active:
                if self.viewing_high_scores:
                    self.high_score.reset_high_scores()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update the position of bullets and get rid of old bullets."""
        self.bullets.update()

        #Get rid of bullets we can't see.
        for bullet in self.bullets.sprites():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """Respond to bullet/alien collisions."""
        #Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_current_high_score()
            self.sb.check_best_level()

        if not self.aliens:
            #Destroy existing bullets and create a new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _create_alien(self, alien_number, row_number):
        """Create aliens and place them in a row."""
        #Create an alien and place it in the row.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _create_fleet(self):
        """Creates the fleet of aliens."""
        #Create an alien and find the number of aliens in a row.
        #Spacing between aliens is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Create the first row of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _update_screen(self):
        """Updates images on the screen and flips to the new screen."""
        screen_bg_image = self.settings.bg
        screen_bg_rect = screen_bg_image.get_rect()
        screen_bg_rect.center = self.screen.get_rect().center
        self.screen.blit(screen_bg_image, screen_bg_rect)

        #Draw the play button if the game is inactive.
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        #Draw the scoreboard.
        self.sb.show_score()

        if self.stats.game_paused:
            self.pause_button.draw_button()

        pygame.display.flip()

    def _welcome_screen(self):
        """Shows a welcome screen with play, instructions, high scores, and quit buttons."""
        welcome_bg_image = self.settings.bg
        welcome_bg_rect = welcome_bg_image.get_rect()
        welcome_bg_rect.center = self.screen.get_rect().center
        welcome_image = pygame.image.load(r"images\welcome_resized.png")
        welcome_rect = welcome_image.get_rect()
        welcome_rect.center = self.screen.get_rect().center
        welcome_rect.top = 0
        self.screen.blit(welcome_bg_image, welcome_bg_rect)
        self.screen.blit(welcome_image, welcome_rect)
        self.play_button.draw_button()
        self.instructions_button.draw_button()
        self.high_score_button.draw_button()
        self.quit_button.draw_button()
        pygame.display.flip()
        #TODO: Add the welcome picture once Melody has finished drawing.
        #TODO: Adjust the button positions if they are in a weird place.

    def _instruction_screen(self):
        """Shows an instructions screen with a back button."""
        screen_bg_image = self.settings.bg
        screen_bg_rect = screen_bg_image.get_rect()
        screen_bg_rect.center = self.screen.get_rect().center
        self.screen.blit(screen_bg_image, screen_bg_rect)
        instructions_image = pygame.image.load(r"images\instructions_resized.png")
        instructions_rect = instructions_image.get_rect()
        instructions_rect.center = self.screen.get_rect().center
        instructions_rect.top = 50
        self.screen.blit(instructions_image, instructions_rect)
        self.back_button.draw_button()
        pygame.display.flip()
    
    def _high_score_screen(self):
        """Show the high score screen so the user can admire their work."""
        file_name = "high_scores.json"
        scores_to_show = self.high_score.read_from_file(file_name)
        name_header = "Name"
        score_header = "Score"
        level_header = "Level"
        score1_name = f"1. {scores_to_show[0]['Name']}"
        score1_score = f"{scores_to_show[0]['Score']:,}"
        score1_level = str(scores_to_show[0]["Level"])
        score2_name = f"2. {scores_to_show[1]['Name']}"
        score2_score = f"{scores_to_show[1]['Score']:,}"
        score2_level = str(scores_to_show[1]["Level"])
        score3_name = f"3. {scores_to_show[2]['Name']}"
        score3_score = f"{scores_to_show[2]['Score']:,}"
        score3_level = str(scores_to_show[2]["Level"])
        score4_name = f"4. {scores_to_show[3]['Name']}"
        score4_score = f"{scores_to_show[3]['Score']:,}"
        score4_level = str(scores_to_show[3]["Level"])
        score5_name = f"5. {scores_to_show[4]['Name']}"
        score5_score = f"{scores_to_show[4]['Score']:,}"
        score5_level = str(scores_to_show[4]["Level"])
        
        #Make Images.
        name_header_image = self.ul_font.render(name_header, True, self.settings.font_color, None)
        score_header_image = self.ul_font.render(score_header, True, self.settings.font_color, None)
        level_header_image = self.ul_font.render(level_header, True, self.settings.font_color, None)
        score1_name_image = self.font.render(score1_name, True, self.settings.font_color, None)
        score1_score_image = self.font.render(score1_score, True, self.settings.font_color, None)
        score1_level_image = self.font.render(score1_level, True, self.settings.font_color, None)
        score2_name_image = self.font.render(score2_name, True, self.settings.font_color, None)
        score2_score_image = self.font.render(score2_score, True, self.settings.font_color, None)
        score2_level_image = self.font.render(score2_level, True, self.settings.font_color, None)
        score3_name_image = self.font.render(score3_name, True, self.settings.font_color, None)
        score3_score_image = self.font.render(score3_score, True, self.settings.font_color, None)
        score3_level_image = self.font.render(score3_level, True, self.settings.font_color, None)
        score4_name_image = self.font.render(score4_name, True, self.settings.font_color, None)
        score4_score_image = self.font.render(score4_score, True, self.settings.font_color, None)
        score4_level_image = self.font.render(score4_level, True, self.settings.font_color, None)
        score5_name_image = self.font.render(score5_name, True, self.settings.font_color, None)
        score5_score_image = self.font.render(score5_score, True, self.settings.font_color, None)
        score5_level_image = self.font.render(score5_level, True, self.settings.font_color, None)

        #Make Rects
        screen_rect = self.screen.get_rect()
        name_header_rect = name_header_image.get_rect()
        score_header_rect = score_header_image.get_rect()
        level_header_rect = level_header_image.get_rect()
        score1_name_rect = score1_name_image.get_rect()
        score1_score_rect = score1_score_image.get_rect()
        score1_level_rect = score1_level_image.get_rect()
        score2_name_rect = score2_name_image.get_rect()
        score2_score_rect = score2_score_image.get_rect()
        score2_level_rect = score2_level_image.get_rect()
        score3_name_rect = score3_name_image.get_rect()
        score3_score_rect = score3_score_image.get_rect()
        score3_level_rect = score3_level_image.get_rect()
        score4_name_rect = score4_name_image.get_rect()
        score4_score_rect = score4_score_image.get_rect()
        score4_level_rect = score4_level_image.get_rect()
        score5_name_rect = score5_name_image.get_rect()
        score5_score_rect = score5_score_image.get_rect()
        score5_level_rect = score5_level_image.get_rect()

        #position Rects
        name_header_rect.left = (screen_rect.width / 2) - 450
        name_header_rect.top = 150

        score_header_rect.left = (screen_rect.width / 2) + 50
        score_header_rect.top = 150

        level_header_rect.left = (screen_rect.width / 2) + 350
        level_header_rect.top = 150

        score1_name_rect.left = name_header_rect.left
        score1_name_rect.top = name_header_rect.bottom + 20
        score2_name_rect.left = name_header_rect.left
        score2_name_rect.top = score1_name_rect.bottom + 20
        score3_name_rect.left = name_header_rect.left
        score3_name_rect.top = score2_name_rect.bottom + 20
        score4_name_rect.left = name_header_rect.left
        score4_name_rect.top = score3_name_rect.bottom + 20
        score5_name_rect.left = name_header_rect.left
        score5_name_rect.top = score4_name_rect.bottom + 20

        score1_score_rect.left = score_header_rect.left
        score1_score_rect.top = score_header_rect.bottom + 20
        score2_score_rect.left = score_header_rect.left
        score2_score_rect.top = score1_score_rect.bottom + 20
        score3_score_rect.left = score_header_rect.left
        score3_score_rect.top = score2_score_rect.bottom + 20
        score4_score_rect.left = score_header_rect.left
        score4_score_rect.top = score3_score_rect.bottom + 20
        score5_score_rect.left = score_header_rect.left
        score5_score_rect.top = score4_score_rect.bottom + 20
        
        score1_level_rect.left = level_header_rect.left
        score1_level_rect.top = level_header_rect.bottom + 20
        score2_level_rect.left = level_header_rect.left
        score2_level_rect.top = score1_level_rect.bottom + 20
        score3_level_rect.left = level_header_rect.left
        score3_level_rect.top = score2_level_rect.bottom + 20
        score4_level_rect.left = level_header_rect.left
        score4_level_rect.top = score3_level_rect.bottom + 20
        score5_level_rect.left = level_header_rect.left
        score5_level_rect.top = score4_level_rect.bottom + 20

        background_rect = pygame.Rect((name_header_rect.left - 20), 25, 950, 480)
        background_border_rect = pygame.Rect(0, 0, 960, 490)
        background_border_rect.center = background_rect.center
        #Get Blit
        screen_bg_image = self.settings.bg
        screen_bg_rect = screen_bg_image.get_rect()
        screen_bg_rect.center = self.screen.get_rect().center
        self.screen.blit(screen_bg_image, screen_bg_rect)
        self.screen.fill(self.play_button.border_color, background_border_rect)
        self.screen.fill(self.play_button.button_color, background_rect)
        self.screen.blit(self.hs_banner_text_image, self.hs_banner_text_rect)
        self.screen.blit(name_header_image, name_header_rect)
        self.screen.blit(score_header_image, score_header_rect)
        self.screen.blit(level_header_image, level_header_rect)

        self.screen.blit(score1_name_image, score1_name_rect)
        self.screen.blit(score1_score_image, score1_score_rect)
        self.screen.blit(score1_level_image, score1_level_rect)
        
        self.screen.blit(score2_name_image, score2_name_rect)
        self.screen.blit(score2_score_image, score2_score_rect)
        self.screen.blit(score2_level_image, score2_level_rect)
        
        self.screen.blit(score3_name_image, score3_name_rect)
        self.screen.blit(score3_score_image, score3_score_rect)
        self.screen.blit(score3_level_image, score3_level_rect)
        
        self.screen.blit(score4_name_image, score4_name_rect)
        self.screen.blit(score4_score_image, score4_score_rect)
        self.screen.blit(score4_level_image, score4_level_rect)
        
        self.screen.blit(score5_name_image, score5_name_rect)
        self.screen.blit(score5_score_image, score5_score_rect)
        self.screen.blit(score5_level_image, score5_level_rect)

        self.reset_scores_button.draw_button()
        self.back_button.draw_button()
        pygame.display.flip()

    def _update_aliens(self):
        """Check alien edges for collision with screen edge then update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        #Look for alien/ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #looking for aliens colliding with bottom of screen, not checking the alien's bottom...
        self._check_aliens_bottom()

    def _change_fleet_direction(self):
        """Drop the entire fleet and change directions."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            #Decrement ships_left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #Get rid of remaining ships and bullets.
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            #Pause.
            sleep(0.5)
        else:
            file_name = "high_scores.json"
            self.stats.game_active = False
            high_scores = self.high_score.read_from_file(file_name)
            if self.high_score.check_high_score(self.stats.score, high_scores):
                user_name = self.high_score.show_input_screen()
                new_high_scores = self.high_score.add_high_score(user_name, self.stats.level, self.stats.score, high_scores)
                self.high_score.write_to_file(file_name, new_high_scores)
                self.viewing_high_scores = True
                self._high_score_screen()
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check to see if any aliens have hit the bottom of the screen, not check the alien's bottom..."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        """Checks to see if a user clicked the play button."""
        if not self.showing_instructions and not self.viewing_high_scores:
            if self.play_button.bg_rect.collidepoint(mouse_pos):
                self.prep_game()

    def _check_pause_button(self, mouse_pos):
        """Checks to see if the user clicked the pause button."""
        if self.pause_button.bg_rect.collidepoint(mouse_pos):
            self.stats.game_paused = False
            pygame.mouse.set_visible(False)

    def _check_quit_button(self, mouse_pos):
        """Checks to see if the user clicked the quit button."""
        if not self.showing_instructions and not self.viewing_high_scores:
            if self.quit_button.bg_rect.collidepoint(mouse_pos):
                sys.exit(0)

    def _check_instructions_button(self, mouse_pos):
        """Checks to see if the user clicked the instructions button."""
        if not self.viewing_high_scores:
            if self.instructions_button.bg_rect.collidepoint(mouse_pos):
                self.showing_instructions = True

    def _check_high_score_button(self, mouse_pos):
        """Checks to see if the user clicked the high scores button."""
        if not self.showing_instructions:
            if self.high_score_button.bg_rect.collidepoint(mouse_pos):
                self.viewing_high_scores = True
            
    def _check_back_button(self, mouse_pos):
        """Checks to see if the user clicked the back button."""
        if self.viewing_high_scores or self.showing_instructions:
            if self.back_button.bg_rect.collidepoint(mouse_pos):
                self.showing_instructions = False
                self.viewing_high_scores = False
                self._welcome_screen()
                
    def _check_reset_button(self, mouse_pos):
        """Checks to see if the user clicked the high score reset button."""
        if self.viewing_high_scores:
            if self.reset_scores_button.bg_rect.collidepoint(mouse_pos):
                self.high_score.reset_high_scores()

    def prep_game(self):
        """Starts the game when player clicks play button or presses 'P' key."""
        if not self.stats.game_active:
            #Reset dynamic settings.
            self.settings.initialize_dynamic_settings()

            #Hide the mouse cursor while we play.
            pygame.mouse.set_visible(False)
            self.stats.reset_stats()
            self.sb.prep_level()
            self.sb.prep_score()
            self.sb.prep_ships()
            self.stats.game_active = True

            #Get rid of remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.stats.game_active:
                if not self.stats.game_paused:
                    self.ship.update()
                    if self.bullets.firing_bullets:
                        self.current_bullet_time = pygame.time.get_ticks()
                        if self.current_bullet_time - self.previous_bullet_time > self.settings.bullet_cooldown:
                            if len(self.bullets) < self.settings.bullets_allowed:
                                self._fire_bullet()
                                self.previous_bullet_time = self.current_bullet_time
                    self._update_bullets()
                    self._update_aliens()
                self._update_screen()
                self.clock.tick(80)
            if not self.stats.game_active and not self.showing_instructions and not self.viewing_high_scores:
                self._welcome_screen()
            elif not self.stats.game_active and self.showing_instructions:
                self._instruction_screen()
            elif not self.stats.game_active and self.viewing_high_scores:
                self._high_score_screen()
if __name__ == '__main__':
    #Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()
