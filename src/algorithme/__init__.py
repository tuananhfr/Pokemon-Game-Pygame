from abc import ABC, abstractmethod
class algorithme(ABC):
    """
    Abstract base class for all algorithms used in the game
    """
    @abstractmethod
    def algo(self,board, tile1_i, tile1_j, tile2_i, tile2_j):
        """
        Abstract method for the main algorithm

        :param board: 2D array representing the current state of the game board
        :param tile1_i: row of the first tile
        :param tile1_j: column of the first tile
        :param tile2_i: row of the second tile
        :param tile2_j: column of the second tile
        """
        pass

    
