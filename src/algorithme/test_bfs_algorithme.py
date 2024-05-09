
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bfsAlgorithme import bfsAlgorithme



class test_bfs_algorithme(unittest.TestCase):

    def test_algo(self):
        board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 16, 20, 2, 32, 17, 25, 9, 32, 33, 20, 29, 30, 0], [0, 5, 30, 6, 28, 28, 21, 25, 5, 33, 6, 9, 2, 0], [0, 25, 4, 7, 17, 16, 8, 6, 21, 5, 29, 7, 12, 0], [0, 30, 6, 12, 22, 30, 16, 4, 2, 20, 29, 11, 17, 0], [0, 21, 12, 33, 11, 28, 21, 32, 4, 11, 9, 8, 22, 0], [0, 12, 28, 7, 25, 32, 7, 13, 11, 13, 17, 22, 16, 0], [0, 22, 5, 9, 20, 8, 29, 4, 8, 13, 33, 13, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        bfs = bfsAlgorithme(board)
        algo_bfs = bfs.algo(1, 2, 1, 10)
        self.assertEqual(algo_bfs[0],(1, 2, 0, 'noDirection'))
        self.assertEqual(algo_bfs[1],(0, 2, 0, 'up'))
        self.assertEqual(bfs.algo(1, 2, 1, 10)[3][3],'right')
        self.assertEqual(algo_bfs[5],(0, 6, 1, 'right'))

       
    def test_algo1(self):
        board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 5, 15, 3, 13, 28, 12, 7, 31, 27, 13, 10, 0], [0, 25, 13, 25, 16, 21, 23, 15, 17, 14, 17, 31, 10, 0], [0, 15, 25, 14, 23, 5, 7, 24, 33, 14, 27, 28, 28, 0], [0, 10, 27, 23, 4, 1, 4, 1, 32, 3, 12, 33, 5, 0], [0, 28, 24, 5, 7, 15, 32, 16, 24, 33, 12, 12, 24, 0], [0, 21, 4, 16, 17, 21, 23, 25, 3, 7, 31, 33, 4, 0], [0, 32, 10, 31, 1, 16, 3, 17, 14, 13, 21, 27, 32, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        bfs = bfsAlgorithme(board)
        
        self.assertEqual(len(bfs.algo(1, 5, 1, 11)[0]),4)
        self.assertEqual(len(bfs.algo(1, 5, 1, 11)),9)
        self.assertEqual(bfs.algo(1, 5, 1, 11), [(1, 5, 0, 'noDirection'), (0, 5, 0, 'up'), (0, 6, 1, 'right'), (0, 7, 1, 'right'), (0, 8, 1, 'right'), (0, 9, 1, 'right'), (0, 10, 1, 'right'), (0, 11, 1, 'right'), (1, 11, 2, 'down')] )
       

if __name__ == '__main__':

    unittest.main()
