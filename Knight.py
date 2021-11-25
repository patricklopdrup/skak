from Coordinate import Coordinate as C
from Move import Move
from Piece import Piece

WHITE = True
BLACK = False


class Knight(Piece):

    stringRep = 'N'
    value = 3
    score_table = [
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
    ]

    def __init__(self, board, side, position,  movesMade=0):
        super(Knight, self).__init__(board, side, position)
        self.movesMade = movesMade


    def getValue(self, coor: C):
        table_val = self.score_table[coor[0]][coor[1]]
        return self.value + table_val


    def getPossibleMoves(self):
        board = self.board
        currentPos = self.position
        movements = [C(2, 1), C(2, -1), C(-2, 1), C(-2, -1), C(1, 2),
                     C(1, -2), C(-1, -2), C(-1, 2)]
        for movement in movements:
            newPos = currentPos + movement
            if board.isValidPos(newPos):
                pieceAtNewPos = board.pieceAtPosition(newPos)
                if pieceAtNewPos is None:
                    yield Move(self, newPos)
                elif pieceAtNewPos.side != self.side:
                    yield Move(self, newPos, pieceToCapture=pieceAtNewPos)
