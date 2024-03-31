from gameSettings import gameSettings

from abc import ABC, abstractmethod


class Screen(ABC):
    """
    Abstract base class representing a screen in the game.

    Attributes:
        game: The game object associated with the screen.
    """

    def __init__(self, game):
        """
        Initialize the Screen object.

        :param self: The GameScreen object that this method is called on.
        :param game: The game object associated with the screen.
        """
        self.game = game

    @abstractmethod
    def display(self):
        """
        Abstract method to display the screen.
        """
        pass

    @abstractmethod
    def draw_dark_image(self,image, image_rect, color):
        """
        Abstract method to draw a darkened image on the screen.

        :param self: The GameScreen object that this method is called on.
        :param image: The image to be darkened.
        :param image_rect: The rectangle defining the position and size of the image.
        :param color: The color to darken the image with.
        """
        pass

    @abstractmethod
    def handle_events(self, event):
        """
        Abstract method to handle events on the screen.

        :param self: The GameScreen object that this method is called on.
        :param event: The event to be handled.
        """
        pass
