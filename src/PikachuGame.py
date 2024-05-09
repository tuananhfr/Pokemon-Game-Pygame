from gameSettings import gameSettings
from Screen.introScreen import introScreen
from Screen.startScreen import startScreen
from Screen.playScreen import playScreen

from Music.startMusic import startMusic
from Sound.effectSound import effectSound
from Sound.gameOverSound import gameOverSound

import pygame
import sys


class PikachuGame:
    """
    Class representing the main game logic and flow of the Pikachu Game.

    Attributes:
        gameWidth (int): Width of the game screen.
        gameHeight (int): Height of the game screen.
        screen (pygame.Surface): Pygame surface representing the game window.
        start_music (startMusic): Instance of startMusic for playing game music.
        click_sound (effectSound): Instance of effectSound for click sound effects.
        play_fail_sound (effectSound): Instance of effectSound for play fail sound effects.
        clicked_tile_sound (effectSound): Instance of effectSound for clicked tile sound effects.
        play_success_sound (effectSound): Instance of effectSound for play success sound effects.
        game_over_music (gameOverSound): Instance of gameOverSound for game over music.
        victory_music (gameOverSound): Instance of gameOverSound for game victory music.
        sound_image (pygame.Surface): Pygame surface for sound button image.
        sound_on (bool): Flag to indicate whether sound is on or off.
        intro_screen (introScreen): Instance of introScreen for the game introduction.
        start_screen (startScreen): Instance of startScreen for the start menu.
        play_screen (playScreen): Instance of playScreen for the gameplay screen.
        current_screen: Current active screen of the game.
    """

    def __init__(self):
        """
        Initialize the PikachuGame object.
        """
        pygame.init()
        
        # Game-related variables and initialization code here
        self.gameWidth = gameSettings.GAMEWIDTH
        self.gameHeight = gameSettings.GAMEHEIGHT

        # Loading the pygame screen.
        self.screen = pygame.display.set_mode((self.gameWidth, self.gameHeight))
        pygame.display.set_caption('Pikachu Game')
        gameIcon = pygame.image.load('assets/images/logo/logo.jpeg')
        pygame.display.set_icon(gameIcon)

        # music       
        self.start_music = startMusic("assets/sounds/Pikachu Kawaii 2002 Song 1.mp3")
        
        # sound effect
        self.click_sound = effectSound("assets/sounds/tap.mp3")
        self.play_fail_sound = effectSound("assets/sounds/fail.mp3")
        self.clicked_tile_sound = effectSound("assets/sounds/click_title.wav")
        self.play_success_sound = effectSound("assets/sounds/success.mp3")
        self.game_over_music= gameOverSound("assets/sounds/gameover.wav")
        self.victory_music= gameOverSound("assets/sounds/victory.wav")


        # sound button
        self.sound_image = pygame.transform.scale(pygame.image.load("assets/images/button/music.png"), (50, 50))
        self.sound_on = True

        #current screen 
        self.intro_screen = introScreen(self)
        self.start_screen = startScreen(self)
        self.play_screen = playScreen(self)
        self.current_screen = self.intro_screen
        self.current_screen.display()

    def set_screen(self, screen):
        """
        Set the current active screen of the game.


        :param self: The GameScreen object that this method is called on.
        :param screen: The screen object to set as the current active screen.
        """
        self.current_screen = screen
        self.current_screen.__init__(self)

    def run_game_loop(self): 
        """
        Main game loop.
        """
        self.set_screen(self.start_screen)
        self.current_screen.display()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.current_screen.handle_events(event)

        # Quit Pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = PikachuGame()
    game.run_game_loop()
