import random
from sys import maxsize
import time
import math

from Board import Board

WHITE = True
BLACK = False

class CustomAI:

    start_time = None
    max_time_sec = 10
    depth = 2
    board = None
    side = None
    
    def __init__(self, board: Board, side: bool, depth: int, max_time_sec: int):
        self.board = board
        self.side = side
        self.depth = depth
        self.max_time_sec = max_time_sec
        self.start_time = time.time()


    '''
    Helper function to find the best move with minimax
    '''
    def bestMoveMinMax(self, new_depth):
        global next_move, game_state_counter, is_time_limit, pruning_counter
        pruning_counter = 0
        is_time_limit = False
        game_state_counter = 0
        self.start_time = time.time() # Reset start time
        next_move = None
        self.depth = new_depth if new_depth != -1 else self.depth
        ### The function
        #self.minMax(self.board, self.depth, self.side)
        self.alphaBeta(self.board, self.depth, -math.inf, math.inf, self.side)
        ###
        print(f"Kiggede på {game_state_counter} spil med {self.depth} træk i dybden.")
        print(f"Pruned {pruning_counter} branches.")
        if is_time_limit:
            print(f"Stoppede søgning efter {self.max_time_sec} sekunder.")
        else:
            time_passed = time.time() - self.start_time
            print(f"Brugte {time_passed} sekunder.")
        return next_move
    

    '''
    Minimax algorithm
    '''
    def minMax(self, board: Board, depth, isWhiteTurn):
        global next_move, game_state_counter, is_time_limit
        game_state_counter += 1
        if time.time() - self.start_time >= self.max_time_sec:
            is_time_limit = True
            return self.scoreBoard(board, isWhiteTurn)
        if depth == 0:
            return self.scoreBoard(board, isWhiteTurn)
        
        # For white aka maximizer
        if isWhiteTurn:
            max_score = -math.inf
            # Loop through all whites moves
            for move in board.getAllMovesLegal(WHITE):
                board.makeMove(move)
                score = self.minMax(board, depth - 1, False)
                if score > max_score:
                    max_score = score
                    # Set the next_move to current move if we hit the depth or our max time is reached
                    #if depth == self.depth:
                    if self.side == WHITE:
                        next_move = move
                board.undoLastMove()
            print(f"max score for white move: {max_score}")
            return max_score

        # For black aka minimizer
        else:
            min_score = math.inf
            for move in board.getAllMovesLegal(BLACK):
                board.makeMove(move)
                score = self.minMax(board, depth - 1, True)
                if score < min_score:
                    min_score = score
                    #if depth == self.depth:
                    if self.side == BLACK:
                        next_move = move
                board.undoLastMove()
            print(f"min score for black move: {min_score}")
            return min_score


    '''
    Minimax algorithm with alpha beta pruning
    '''
    def alphaBeta(self, board: Board, depth, alpha, beta, isWhiteTurn):
        global next_move, game_state_counter, is_time_limit, pruning_counter
        game_state_counter += 1
        if time.time() - self.start_time >= self.max_time_sec:
            is_time_limit = True
            return self.scoreBoard(board, isWhiteTurn)
        if depth == 0:
            return self.scoreBoard(board, isWhiteTurn)
        
        # For white aka maximizer
        if isWhiteTurn:
            max_score = -math.inf
            # Loop through all whites moves
            moves = board.getAllMovesLegal(WHITE)
            random.shuffle(moves)
            for move in moves:
                board.makeMove(move)
                score = self.alphaBeta(board, depth - 1, alpha, beta, False)
                if score > max_score:
                    max_score = score
                    # Set the next_move to current move if we hit the depth or our max time is reached
                    if depth == self.depth:
                        if self.side == WHITE:
                            next_move = move
                board.undoLastMove()
                # Pruning
                alpha = max(alpha, score)
                if beta <= alpha:
                    pruning_counter += 1
                    break
            return max_score

        # For black aka minimizer
        else:
            min_score = math.inf
            moves = board.getAllMovesLegal(BLACK)
            random.shuffle(moves)
            for move in moves:
                board.makeMove(move)
                score = self.alphaBeta(board, depth - 1, alpha, beta, True)
                if score < min_score:
                    min_score = score
                    if depth == self.depth:
                        if self.side == BLACK:
                            next_move = move
                board.undoLastMove()
                # Pruning
                beta = min(beta, score)
                if beta <= alpha:
                    pruning_counter += 1
                    break
            return min_score


    '''
    Positive numbers for white. Negative number for black
    '''
    def scoreBoard(self, board: Board, side: bool):
        if side == WHITE:
            point = board.getPointAdvantageOfSide(WHITE)
            if point > 0:
                print(f"hvid point: {point}")
            return point
        else:
            point = board.getPointAdvantageOfSide(BLACK)
            if point < 0:
                print(f"sort point: {point}")
            return point
        # if side == WHITE:
        #     return board.getPointValueOfSide(WHITE)
        # else:
        #     return -(board.getPointValueOfSide(BLACK))