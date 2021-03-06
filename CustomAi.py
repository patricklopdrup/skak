import random
from sys import maxsize
import time
import math

from numpy.core.fromnumeric import transpose

from Coordinate import Coordinate as C
from Board import Board
from Move import Move
from Piece import Piece
from TranspositionTable import TranspositionTable
from Zobrist import compute_hash

WHITE = True
BLACK = False

class CustomAI:

    start_time = None
    max_time_sec = 10
    init_depth = 1
    current_depth = 0
    timeout = False

    test_piece = None
    best_move = None
    global_best_move = None

    board = None
    side = None

    # For statistic
    pruning_counter = 0
    state_counter = 0
    best_move_in_layer = 0

    
    def __init__(self, board: Board, side: bool):
        self.board = board
        self.side = side
        self.best_move = Move(Piece(board, WHITE, C(0,0)), 0,1)
        self.global_best_move = Move(Piece(board, WHITE, C(0,0)), 0,1)


    '''
    Helper function to find the best move with minimax
    '''
    def bestMoveMinMax(self, total_moves):
        self.best_move = Move(Piece(self.board, WHITE, C(0,0)), 0,1)
        self.global_best_move = Move(Piece(self.board, WHITE, C(0,0)), 0,1)
        self.timeout = False
        self.current_depth = 0
        self.pruning_counter = 0
        self.state_counter = 0
        self.best_move_in_layer = 0
        self.total_moves = total_moves
        # init transposition table
        self.trans_table = TranspositionTable
        self.start_time = time.time()

        for d in range(100):
            # Update global best move only when completely done with a search tree
            if self.global_best_move != self.best_move:
                self.global_best_move = self.best_move
                self.best_move_in_layer = self.current_depth
            
            self.current_depth = self.init_depth + d

            self.alphaBeta(self.board, self.current_depth, -math.inf, math.inf, self.side)
            #self.negamax(self.board, self.current_depth, -math.inf, math.inf, self.side)
            if self.timeout:
                break

        print(f"Kiggede p?? {self.state_counter} gamestates p?? {time.time() - self.start_time} sekunder.")
        print(f"Prunede {self.pruning_counter} branches og n??ede ned til dybde {self.current_depth}.")
        print(f"Fandt det bedste tr??k i dybde {self.best_move_in_layer}")
        #self.board.getAllMovesLegal(WHITE)
        if self.global_best_move is None:
            _legal_moves = self.board.getAllMovesLegal(self.side)
            return random.choice(_legal_moves)
        else:
            return self.global_best_move
    

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
        self.state_counter += 1
        if time.time() - self.start_time >= self.max_time_sec:
            self.timeout = True
            return self.scoreBoard(board, depth)
        if depth == 0:
            return self.scoreBoard(board, depth)
        
        # For white aka maximizer
        if isWhiteTurn:
            max_score = -math.inf
            # Loop through all whites moves
            if self.total_moves <= 1:
                moves = board.getAllFirstMovesLegal(WHITE)
            else:
                moves = board.getAllMovesLegal(WHITE)
            for move in moves:
                board.makeMove(move)
                score = self.alphaBeta(board, depth - 1, alpha, beta, False)
                if score > max_score:
                    max_score = score
                    # Set the next_move to current move if we hit the depth or our max time is reached
                    if depth == self.current_depth:
                        if self.side == WHITE:
                            self.best_move = move
                            #print(f"{score} in d={self.current_depth} for {move}")
                board.undoLastMove()
                # Pruning
                alpha = max(alpha, max_score)
                if max_score >= beta:
                    self.pruning_counter += 1
                    break
            return max_score

        # For black aka minimizer
        else:
            min_score = math.inf
            if self.total_moves <= 1:
                moves = board.getAllFirstMovesLegal(BLACK)
            else:
                moves = board.getAllMovesLegal(BLACK)
            for move in moves:
                board.makeMove(move)
                score = self.alphaBeta(board, depth - 1, alpha, beta, True)
                if score < min_score:
                    min_score = score
                    if depth == self.current_depth:
                        if self.side == BLACK:
                            self.best_move = move
                board.undoLastMove()
                # Pruning
                beta = min(beta, min_score)
                if min_score <= alpha:
                    self.pruning_counter += 1
                    break
            return min_score



    '''
    Negamax with alpha beta pruning
    '''
    def negamax(self, board: Board, depth, alpha, beta, isWhiteTurn):
        self.state_counter += 1
        if time.time() - self.start_time >= self.max_time_sec:
            self.timeout = True
            return self.scoreBoard(board, isWhiteTurn)
        if depth == 0:
            return self.scoreBoard(board, isWhiteTurn)
        
        moves = board.getAllMovesLegal(isWhiteTurn)
        value = -math.inf
        for move in moves:
            board.makeMove(move)
            score = -self.negamax(board, depth-1, -beta, -alpha, not isWhiteTurn)
            if score > value:
                value = score
                if depth == self.current_depth:
                    if self.side == isWhiteTurn:
                        self.best_move = move
            board.undoLastMove()
            alpha = max(alpha, value)
            if alpha >= beta:
                self.pruning_counter += 1
                break
        return value


    '''
    Positive numbers for white. Negative number for black
    '''
    def scoreBoard(self, board: Board, depth):
        depth *= 10
        score = board.getPointAdvantageWithTable(WHITE)
        if score > 0:
            return int(score + ((score * depth) / 100))
        else:
            return score