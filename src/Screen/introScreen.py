from Screen import Screen
from gameSettings import gameSettings
from Music.introMusic import introMusic
import pygame


class introScreen(Screen):
    """
    Class representing the introduction screen of the game.

    Attributes:
        game: The game object associated with the screen.
        logo_image: Pygame surface representing the logo image.
    """

    def __init__(self, game):
        """
        Initialize the introScreen object.

        :param self: The GameScreen object that this method is called on.
        :param game: The game object associated with the screen.
        """
        super().__init__(game)
         
        # Load images logo        
        self.logo_image = pygame.image.load("assets/images/logo/logo.jpeg")

    def display(self):
        """
        Display the introduction screen.
        """
        # background
        self.game.screen.fill(gameSettings.WHITE)
        # logo background
        self.game.screen.blit(self.logo_image, ((self.game.gameWidth - self.logo_image.get_width()) // 2,
                                                (self.game.gameHeight - self.logo_image.get_height()) // 2))
        pygame.display.flip()
        # music
        intro_music = introMusic('assets/sounds/intro.mp3')
        intro_music.play()

    def draw_dark_image(self):
        pass
    
    def handle_events(self, event):
        pass
