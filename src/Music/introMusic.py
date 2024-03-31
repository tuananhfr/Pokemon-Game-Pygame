import pygame
import time
from Music import Music

class introMusic(Music):
    """
    Class representing the intro music in the game.
    """
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