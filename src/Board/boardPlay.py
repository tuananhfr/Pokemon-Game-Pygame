from gameSettings import gameSettings
from algorithme.bfsAlgorithme import bfsAlgorithme

import pygame
import random, collections
class boardPlay():
    """
    Class to manage the game board including drawing tiles, borders, paths, hints, and resetting the board.

    Attributes:
        game (object): The main game object.
    """
    def __init__(self, game):
        """
        Initializes the boardPlay object.

        :param self: The GameScreen object that this method is called on.
        :param game (object): The main game object.
        """
        self.game = game
        for i in range(1, gameSettings.NUM_TILE + 1): gameSettings.LIST_TILE[i] = pygame.transform.scale(pygame.image.load("assets/images/tiles/section" + str(i) + ".png"), (gameSettings.TILE_WIDTH, gameSettings.TILE_HEIGHT))
        
        
    def get_left_top_coords(self,i, j): # get left top coords of card from index i, j
        """
        Calculates the left-top coordinates of a tile.

        :param self: The GameScreen object that this method is called on.
        
        :param i (int): The row index of the tile.
        :param j (int): The column index of the tile.

        :return: tuple: A tuple containing the x and y coordinates of the top-left corner of the tile.
        """
        x = j * gameSettings.TILE_WIDTH + gameSettings.MARGIN_X
        y = i * gameSettings.TILE_HEIGHT + gameSettings.MARGIN_Y
        return x, y

    def get_center_coords(self,i, j): # get center coords of card from index i, j
        """
        Calculates the center coordinates of a tile.

        :param self: The GameScreen object that this method is called on.       
        :param i (int): The row index of the tile.
        :param j (int): The column index of the tile.

        :return: tuple: A tuple containing the x and y coordinates of the center of the tile.
        """
        x, y = self.get_left_top_coords(i, j)
        return x + gameSettings.TILE_WIDTH // 2, y + gameSettings.TILE_HEIGHT // 2
    
    def get_random_board(self):
        """
        Generates a random board layout.

        :return: list: A 2D list representing the randomized board layout.
        """
        list_index_tiles = list(range(1, gameSettings.NUM_TILE + 1)) #21
        random.shuffle(list_index_tiles)
        list_index_tiles = list_index_tiles[:gameSettings.NUM_TILE_ON_BOARD] * gameSettings.NUM_SAME_TILE #84
        random.shuffle(list_index_tiles)
        board = [[0 for _ in range(gameSettings.BOARD_COLUMNS)]for _ in range(gameSettings.BOARD_ROWS)]
        k = 0
        for i in range(1, gameSettings.BOARD_ROWS - 1):
            for j in range(1, gameSettings.BOARD_COLUMNS - 1):
                board[i][j] = list_index_tiles[k]
                k += 1
        return board
    
    def draw_clicked_tiles(self,board, clicked_tiles):
        """
        Draws clicked tiles on the board.

        :param self: The GameScreen object that this method is called on.       
        
        :param board (list): A 2D list representing the current state of the game board.
        :param clicked_tiles (list): A list of tuples containing the coordinates of the clicked tiles.
        """
        for i, j in clicked_tiles:
            x, y = self.get_left_top_coords(i, j)
            try:
                darkImage = gameSettings.LIST_TILE[board[i][j]].copy()
                darkImage.fill((60, 60, 60), special_flags = pygame.BLEND_RGB_SUB)
                self.game.screen.blit(darkImage, (x, y))
                
            except: pass

    def draw_border_tile(self,board, i, j):
        """
        Draws a blue border around a specific tile on the game board.

        :param board: The game board
        :param i: The row number of the tile
        :param j: The column number of the tile
        """
        
        x, y = self.get_left_top_coords(i, j)
        pygame.draw.rect(self.game.screen, (0, 0, 255),(x - 1, y - 3, gameSettings.TILE_WIDTH + 4, gameSettings.TILE_HEIGHT + 4), 2)

    def draw_path(self,path):
        """
        Draws a series of connected line segments on the screen, representing the path that the player's character has taken through the game board.

        :param path: a list of tuples, where each tuple represents a point in the path, and contains two elements: the row and column number of the tile.
        """
        for i in range(len(path) - 1):
            start_pos = (self.get_center_coords(path[i][0], path[i][1]))
            end_pos = (self.get_center_coords(path[i + 1][0], path[i + 1][1]))
            pygame.draw.line(self.game.screen, 'red', start_pos, end_pos, 4)
            pygame.display.update()
        pygame.time.wait(400)

    def get_hint(self,board):
        """
        Generates a hint for the next move for the player by finding the first two tiles that are connected and returns their coordinates.

        :param board: A 2D array representing the current state of the game board
        :return: A list of two tuples, where each tuple represents the coordinates of a tile
        """
        hint = [] # stories two tuple
        tiles_location = collections.defaultdict(list)
        for i in range(gameSettings.BOARD_ROWS):
    	    for j in range(gameSettings.BOARD_COLUMNS):
                if board[i][j]:
                    tiles_location[board[i][j]].append((i, j))
        for i in range(gameSettings.BOARD_ROWS):
            for j in range(gameSettings.BOARD_COLUMNS):
                if board[i][j]:
                    for o in tiles_location[board[i][j]]:	
                        if o != (i, j) and bfsAlgorithme.algo(board, i, j, o[0], o[1]):
                            hint.append((i, j))
                            hint.append(o)
                            return hint
        return []
    

    def draw_hint(self,hint):
        """
        Draws a green border around the tiles that are part of the hint that is generated by the `get_hint` method.

        :param hint: a list of tuples, where each tuple represents the coordinates of a tile
        """
        for i, j in hint:
            x, y = self.get_left_top_coords(i, j)
            pygame.draw.rect(self.game.screen, (0, 255, 0),(x - +1, y - 2, gameSettings.TILE_WIDTH + 4, gameSettings.TILE_HEIGHT + 4), 2)

    def reset_board(self,board):
        """
        Resets the current state of the game board by shuffling the current tiles and placing them in random positions.

        :param board: A 2D array representing the current state of the game board
        :return: A 2D array representing the new state of the game board
        """
        current_tiles = []
        for i in range(gameSettings.BOARD_ROWS):
            for j in range(gameSettings.BOARD_COLUMNS):
                if board[i][j]: current_tiles.append(board[i][j])
        tmp = current_tiles[:]
        while tmp == current_tiles:
            random.shuffle(current_tiles)
        k = 0
        for i in range(gameSettings.BOARD_ROWS):
            for j in range(gameSettings.BOARD_COLUMNS):
                if board[i][j]:
                    board[i][j] = current_tiles[k]
                    k += 1
        return board


    def draw_board(self,board):
        """
        Draws the current state of the game board on the screen.
        :param board: A 2D array representing the current state of the game board
        """
        for i in range(1, gameSettings.BOARD_ROWS - 1):
            for j in range(1, gameSettings.BOARD_COLUMNS - 1):			
                if board[i][j] != 0:
                    self.game.screen.blit(gameSettings.LIST_TILE[board[i][j]], self.get_left_top_coords(i, j))
                            
    
