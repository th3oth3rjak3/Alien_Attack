# Alien_Attack

This game is a collaboration between my daughter and I to develop a fun game to enhance our knowledge of python 3. 

When the game loads, there are a few screen options to choose from:
    Play the game
    High scores
    Instructions
    Quit Playing

When the user starts playing the game, a new screen loads some game objects:
    the ship
    alien fleet of ships
    score board with current score and best score since opening the application
    ships remaining

To play the game, the user will use the left and right arrow keys to move across the screen. The space bar is used to fire bullets at the alien fleet. The space bar can be pressed and released to fire one bullet or can be held to fire a stream of bullets. 

When aliens are hit, they are removed from the fleet that is moving left and right across the screen. To clear a stage, the user must defeat all aliens in the fleet. 

As the stages increase speed and difficulty increases as well.

The game ends after the user is hit by an alien ship or when the alien fleet reaches the bottom of the screen. After the game ends, if the user has a high score, they will be prompted to enter their name so that they can be placed into the Alien Attack hall of fame!

Scores are recorded to the high_scores.json file using a function in the high_score.py file.

On the instructions screen, it demonstrates how to play the game and some various shortcuts to help the user navigate gameplay.

Future ideas:
    -On the pause menu should we give the user an option to go back to the main menu without having to quit the game?
    -May want to refactor the code so it's a little more clean.
    -Give the alien fleet weapons so the user has to dodge incoming bullets.
    -Enhance user weapons so that they either shoot more bullets, a different bullet spread pattern, or another bullet shape.
    -Fix the hard coded screen resolution at 1920 x 1080 so that it's dynamic or works for more sizes than just this one. May not work for laptop screens of smaller size.
    -Turn into a .exe file with all the dependencies and package into a .msi file to share with friends.