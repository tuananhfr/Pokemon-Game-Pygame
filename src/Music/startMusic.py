import pygame
from Music import Music
class startMusic(Music):
    """
    Class representing the background music during the start screen.
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
        Start playing the background music.
        """
         # Play the background music
        pygame.mixer.music.load(self.src)
        pygame.mixer.music.set_volume(0.15)
        pygame.mixer.music.play(-1, 0.0, 5000)
         
    def stop(self):    
        """
        Stop playing the background music.
        """    
        pygame.mixer.music.stop()