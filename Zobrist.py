import numpy
import random
import math
from Piece import Piece

WHITE = True
BLACK = False

ZobristTable = numpy.zeros((8,8,12))
#https://www.youtube.com/watch?v=wdkf6i1fL5c&t=106s
def index_of(piece_str_rep: str, side: bool):
    if side == WHITE:
        if piece_str_rep == 'P':
            return 0
        if piece_str_rep == 'N':
            return 1
        if piece_str_rep == 'B':
            return 2
        if piece_str_rep == 'R':
            return 3
        if piece_str_rep == 'Q':
            return 4
        if piece_str_rep == 'K':
            return 5
    else:
        if piece_str_rep == 'P':
            return 6
        if piece_str_rep == 'N':
            return 7
        if piece_str_rep == 'B':
            return 8
        if piece_str_rep == 'R':
            return 9
        if piece_str_rep == 'Q':
            return 10
        if piece_str_rep == 'K':
            return 11
        

def init_table():
    for i in range(8):
        for j in range(8):
            for k in range(12):
                ZobristTable[i][j][k] = random.randint(0, 2**64-1)


def compute_hash(board):
    hash = 0
    pieces = board.pieces
    p: Piece
    for p in pieces:
        piece_id = index_of(p.stringRep, p.side)
        x = p.position[1]
        y = p.position[0]
        hash ^= int(ZobristTable[x][y][piece_id].item())
    return hash