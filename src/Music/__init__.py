from abc import ABC, abstractmethod
import pygame
class Music(ABC):
    """
    Abstract base class for music-related functionality in the game.
    Subclasses must implement the abstract methods to define specific music behavior.
    """
    def __init__(self, src):
        """
        Initialize the Music object.
        
        :param self: The GameScreen object that this method is called on.
        :param src (str): The source of the music (file path or identifier).
        """
        pygame.mixer.init()
        self.src = src
        

    @abstractmethod
    def play(self):
        """
        Abstract method to start playing the music.
        Subclasses must implement this method to define how the music is played.
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Abstract method to stop playing the music.
        Subclasses must implement this method to define how the music is stopped.
        """
        pass
