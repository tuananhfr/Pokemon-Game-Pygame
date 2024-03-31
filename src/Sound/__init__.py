from abc import ABC, abstractmethod
import pygame
class Sound(ABC):
    """
    Abstract base class for sound-related functionality in the game.
    Subclasses must implement the abstract methods to define specific sound behavior.
    """
    def __init__(self, src):
        """
        Initialize the Sound object.
        
        :param self: The GameScreen object that this method is called on.
        
        :param src (str): The source of the sound (file path or identifier).
        """
        pygame.mixer.init()
        self.src = src

        

    @abstractmethod
    def play(self):
        """
        Abstract method to play the sound.
        Subclasses must implement this method to define how the sound is played.
        """
        pass

    @abstractmethod
    def setVolume(self):
        """
        Abstract method to set the volume of the sound.
        Subclasses must implement this method to define how the volume is set.
        """
        pass
