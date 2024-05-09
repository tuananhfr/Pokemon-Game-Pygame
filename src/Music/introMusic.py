import pygame
import time
from Music import Music

class introMusic(Music):
    """
    Class representing the intro music in the game.
    """
    def __init__(self, src):
        """
        Initialize the start music with the given source.

        :param self: The GameScreen object that this method is called on.
        :param src: The file path of the music.
        """
        super().__init__(src) 
    def play(self):
        """
        Start playing the intro music.
        """
        pygame.mixer.music.load(self.src)
        pygame.mixer.music.play()
        time.sleep(1)
        pygame.mixer.music.stop()
        
    def stop(self):
        """
        Stop playing the intro music.
        """
        pass