
import queue

class bfsAlgorithme:
    def __init__(self, board):
        """
        :param board: 2D array representing the current state of the game board
        """
        self.board = board
        self.n = len(board)
        self.m = len(board[0])

    def algo(self, tile1_i, tile1_j, tile2_i, tile2_j):
        """
        Finds the shortest path between two tiles on the board using the Breadth-First Search algorithm

        :param tile1_i: row of the first tile
        :param tile1_j: column of the first tile
        :param tile2_i: row of the second tile
        :param tile2_j: column of the second tile
        :return: a list of tuples representing the shortest path between the two tiles
        """

        def backtrace(parent, tile1_i, tile1_j, tile2_i, tile2_j):
            """
            Generate the shortest path between two tiles on the board

            :param parent: dictionary containing the previous nodes
            :param tile1_i: row of the first tile
            :param tile1_j: column of the first tile
            :param tile2_i: row of the second tile
            :param tile2_j: column of the second tile
            :return: a list of tuples representing the shortest path between the two tiles
            """
            start = (tile1_i, tile1_j, 0, 'noDirection')
            end = None
            for node in parent:
                if node[:2] == (tile2_i, tile2_j):
                    end = node
            path = [end]
            while path[-1] != start:
                path.append(parent[path[-1]])
            path.reverse()
            for p in path:
                p = p[:2]

            return path

        if self.board[tile1_i][tile1_j] != self.board[tile2_i][tile2_j]:
            return []

        visited = set()
        visited.add((tile1_i, tile1_j, 0, 'noDirection'))
        parent = {}
        q = queue.Queue()
        q.put((tile1_i, tile1_j, 0, 'noDirection'))

        while not q.empty():
            i, j, numTurn, direction = q.get()
            if (i, j) != (tile1_i, tile1_j) and (i, j) == (tile2_i, tile2_j):
                return backtrace(parent, tile1_i, tile1_j, tile2_i, tile2_j)
                
            directions = {(i - 1, j): 'up', (i + 1, j): 'down', (i, j + 1): 'right', (i, j - 1): 'left'}
            for idxI, idxJ in directions:
                nextDirection = directions[(idxI, idxJ)]
                if idxI >= 0 and idxI < self.n and idxJ >= 0 and idxJ < self.m and (self.board[idxI][idxJ] == 0 or (idxI, idxJ) == (tile2_i, tile2_j)):
                    if direction == 'noDirection' or (direction == nextDirection and (idxI, idxJ, numTurn, nextDirection) not in visited):
                        q.put((idxI, idxJ, numTurn, nextDirection))
                        visited.add((idxI, idxJ, numTurn, nextDirection))
                        parent[(idxI, idxJ, numTurn, nextDirection)] = (i, j, numTurn, direction)
                    elif direction != nextDirection and numTurn < 2 and (idxI, idxJ, numTurn + 1, nextDirection) not in visited:
                        q.put((idxI, idxJ, numTurn + 1, nextDirection))
                        visited.add((idxI, idxJ, numTurn + 1, nextDirection))
                        parent[(idxI, idxJ, numTurn + 1, nextDirection)] = (i, j, numTurn, direction)
        return []
