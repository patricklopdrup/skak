from Coordinate import Coordinate as C
from Piece import Piece
import numpy

WHITE = True
BLACK = False


class Bishop (Piece):

    stringRep = 'B'
    value = 330
    score_table_white = numpy.array([
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ])

    score_table_black = numpy.array([
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ])

    def __init__(self, board, side, position, movesMade=0):
        super(Bishop, self).__init__(board, side, position)
        self.movesMade = movesMade


    def getValue(self, coor: C, side: bool):
        # Reverse x and y so it matches the Board
        x = coor[1]
        y = coor[0]
        if side == WHITE:
            table_val = self.score_table_white[x,y]
        else:
            table_val = self.score_table_black[x,y]
        return self.value + table_val


    def getPossibleMoves(self):
        currentPosition = self.position
        directions = [C(1, 1), C(1, -1), C(-1, 1), C(-1, -1)]
        for direction in directions:
            for move in self.movesInDirectionFromPos(currentPosition,
                                                     direction, self.side):
                yield move
