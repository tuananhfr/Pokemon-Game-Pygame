import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from Board.boardPlay import boardPlay

from gameSettings import gameSettings
from algorithme.bfsAlgorithme import bfsAlgorithme


class test_board_play(unittest.TestCase):

    def setUp(self):
        self.board = boardPlay(None)
        

    def test_get_left_top_coords_with_valid_input(self):
        x, y = self.board.get_left_top_coords(2, 3)
        self.assertEqual(x, 3 * gameSettings.TILE_WIDTH + gameSettings.MARGIN_X)
        self.assertEqual(y, 2 * gameSettings.TILE_HEIGHT + gameSettings.MARGIN_Y)

    def test_get_left_top_coords_with_zero_input(self):
        x, y = self.board.get_left_top_coords(0, 0)
        self.assertEqual(x, gameSettings.MARGIN_X)
        self.assertEqual(y, gameSettings.MARGIN_Y)

    def test_get_left_top_coords_with_negative_input(self):
        x, y = self.board.get_left_top_coords(-1, -1)
        self.assertEqual(x, gameSettings.MARGIN_X - gameSettings.TILE_WIDTH)
        self.assertEqual(y, gameSettings.MARGIN_Y - gameSettings.TILE_HEIGHT)
    def test_get_center_coords(self):
        x, y = self.board.get_center_coords(2, 3)
        self.assertEqual(x, 325)
        self.assertEqual(y, 204)
    def test_get_random_board(self):
        board = self.board.get_random_board()
        self.assertEqual(len(board), gameSettings.BOARD_ROWS)
        self.assertEqual(len(board[0]), gameSettings.BOARD_COLUMNS)
        self.assertEqual(sum(row.count(0) for row in board), gameSettings.BOARD_ROWS * gameSettings.BOARD_COLUMNS - gameSettings.NUM_TILE_ON_BOARD * gameSettings.NUM_SAME_TILE)
    
    def test_get_hint(self):
    
    
        # Define the board for testing
        board_play = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 16, 20, 2, 32, 17, 25, 9, 32, 33, 20, 29, 30, 0],
            [0, 5, 30, 6, 28, 28, 21, 25, 5, 33, 6, 9, 2, 0],
            [0, 25, 4, 7, 17, 16, 8, 6, 21, 5, 29, 7, 12, 0],
            [0, 30, 6, 12, 22, 30, 16, 4, 2, 20, 29, 11, 17, 0],
            [0, 21, 12, 33, 11, 28, 21, 32, 4, 11, 9, 8, 22, 0],
            [0, 12, 28, 7, 25, 32, 7, 13, 11, 13, 17, 22, 16, 0],
            [0, 22, 5, 9, 20, 8, 29, 4, 8, 13, 33, 13, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        # Get the hint
        hint = self.board.get_hint(board_play)

        # Perform assertions
        self.assertEqual(len(hint), 2)
        self.assertIsInstance(hint[0], tuple)
        self.assertIsInstance(hint[1], tuple)

        # Check that the hint is valid by running BFS
        bfs = bfsAlgorithme(board_play)
        self.assertTrue(bfs.algo(*hint[0], *hint[1]))

    def test_reset_board(self):
       # Define the board for testing
        board_play = [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 16, 20, 2, 32, 17, 25, 9, 32, 33, 20, 29, 30, 0],
            [0, 5, 30, 6, 28, 28, 21, 25, 5, 33, 6, 9, 2, 0],
            [0, 25, 4, 7, 17, 16, 8, 6, 21, 5, 29, 7, 12, 0],
            [0, 30, 6, 12, 22, 30, 16, 4, 2, 20, 29, 11, 17, 0],
            [0, 21, 12, 33, 11, 28, 21, 32, 4, 11, 9, 8, 22, 0],
            [0, 12, 28, 7, 25, 32, 7, 13, 11, 13, 17, 22, 16, 0],
            [0, 22, 5, 9, 20, 8, 29, 4, 8, 13, 33, 13, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        resetboard = self.board.reset_board(board_play)
        
       
        self.assertEqual(len(board_play), len(resetboard))

        # Check that the tiles are shuffled
        self.assertNotEqual(resetboard[0],[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

       
    

if __name__ == '__main__':

    unittest.main()


 

