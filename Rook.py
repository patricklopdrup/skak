from Coordinate import Coordinate as C
from Piece import Piece

WHITE = True
BLACK = False


class Rook (Piece):

    stringRep = 'R'
    value = 5
    score_table = [
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [ 0,  0,  0,  5,  5,  0,  0,  0]
    ]

    def __init__(self, board, side, position,  movesMade=0):
        super(Rook, self).__init__(board, side, position)
        self.movesMade = movesMade


    def getValue(self, coor: C):
        table_val = self.score_table[coor[0]][coor[1]]
        return self.value + table_val


    def getPossibleMoves(self):
        currentPosition = self.position

        directions = [C(0, 1), C(0, -1), C(1, 0), C(-1, 0)]
        for direction in directions:
            for move in self.movesInDirectionFromPos(currentPosition,
                                                     direction, self.side):
                yield move
