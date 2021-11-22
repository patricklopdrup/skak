import random
import sys
import time

from AI import AI
from Board import Board
from CustomAi import CustomAI
from InputParser import InputParser
from debug import *

WHITE = True
BLACK = False
TIME_LIMIT_SEC = 15


def askForPlayerSide():
    if debug:
        return WHITE
    playerChoiceInput = input(
        "What side would you like to play as [wB]? ").lower()
    if 'w' in playerChoiceInput:
        print("You will play as white")
        return WHITE
    else:
        print("You will play as black")
        return BLACK


def askForDepthOfAI():
    if debug:
        return 3
    depthInput = 2
    try:
        depthInput = int(input("How deep should the AI look for moves?\n"
                               "Warning : values above 3 will be very slow."
                               " [2]? "))
        while depthInput<=0:
             depthInput = int(input("How deep should the AI look for moves?\n"
                               "Warning : values above 3 will be very slow. "
                               "Your input must be above 0."
                               " [2]? "))

    except KeyboardInterrupt:
        sys.exit()
    except:
        print("Invalid input, defaulting to 2")
    return depthInput


def printCommandOptions():
    undoOption = 'u : undo last move'
    printLegalMovesOption = 'l : show all legal moves'
    randomMoveOption = 'r : make a random move'
    quitOption = 'quit : resign'
    moveOption = 'a3, Nc3, Qxa2, etc : make the move'
    options = [undoOption, printLegalMovesOption, randomMoveOption,
               quitOption, moveOption, '', ]
    print('\n'.join(options))


def printAllLegalMoves(board, parser):
    for move in parser.getLegalMovesWithNotation(board.currentSide, short=True):
        print(move.notation)


def getRandomMove(board, parser):
    legalMoves = board.getAllMovesLegal(board.currentSide)
    randomMove = random.choice(legalMoves)
    randomMove.notation = parser.notationForMove(randomMove)
    return randomMove


def makeMove(move, board):
    print("Making move : " + move.notation)
    board.makeMove(move)


def printPointAdvantage(board):
    print("Currently, the point difference is : " +
          str(board.getPointAdvantageOfSide(board.currentSide)))


def undoLastTwoMoves(board):
    if len(board.history) >= 2:
        board.undoLastMove()
        board.undoLastMove()


def startGame(board: Board, playerSide, ai: CustomAI):
    parser = InputParser(board, playerSide)
    hit_time_limit_counter = 0
    while True:
        print()
        print(board)
        print()
        if board.isCheckmate():
            if board.currentSide == playerSide:
                print("Checkmate, you lost")
            else:
                print("Checkmate! You won!")
            return

        if board.isStalemate():
            if board.currentSide == playerSide:
                print("Stalemate")
            else:
                print("Stalemate")
            return

        if board.currentSide == playerSide:
            # printPointAdvantage(board)
            move = None
            command = input("It's your move."
                            " Type '?' for options. ? ")
            if command.lower() == 'u':
                undoLastTwoMoves(board)
                continue
            elif command.lower() == '?':
                printCommandOptions()
                continue
            elif command.lower() == 'l':
                printAllLegalMoves(board, parser)
                continue
            elif command.lower() == 'r':
                move = getRandomMove(board, parser)
            elif command.lower() == 'exit' or command.lower() == 'quit' or command.lower() == 'q':
                return
            try:
                if command.lower() != 'r':
                    move = parser.parse(command)
            except ValueError as error:
                print("%s" % error)
                continue
            makeMove(move, board)

        else:
            print("AI thinking...")
            #move = ai.getBestMove()

            # Set dynamic depth for the AI
            new_depth = -1
            if hit_time_limit_counter >= 2:
                new_depth = ai.depth - 1
                hit_time_limit_counter = 0
            elif hit_time_limit_counter <= -2:
                new_depth = ai.depth + 1
                hit_time_limit_counter = 0
            
            print(f"Time limit hit: {hit_time_limit_counter}. Ny depth: {new_depth}")
            
            start_time = time.time()
            move = ai.bestMoveMinMax(new_depth)
            end_time = time.time()
            ai_total_time = end_time - start_time
            # AI used less than 40% of the time it had
            if ai_total_time <= TIME_LIMIT_SEC * 0.4:
                hit_time_limit_counter -= 2
            # AI used less than 75% of the time it had
            elif ai_total_time <= TIME_LIMIT_SEC * 0.75:
                hit_time_limit_counter -= 1
            # If the AI hit the time limit
            elif ai_total_time >= TIME_LIMIT_SEC:
                hit_time_limit_counter += 2

            move.notation = parser.notationForMove(move)
            makeMove(move, board)

def twoPlayerGame(board):
    parserWhite = InputParser(board, WHITE)
    parserBlack = InputParser(board, BLACK)
    while True:
        print()
        print(board)
        print()
        if board.isCheckmate():
            print("Checkmate")
            return

        if board.isStalemate():
            print("Stalemate")
            return

        # printPointAdvantage(board)
        if board.currentSide == WHITE:
            parser = parserWhite
        else:
            parser = parserBlack
        move = None
        command = input("It's your move, {}.".format(board.currentSideRep()) + \
                        " Type '?' for options. ? ")
        if command.lower() == 'u':
            undoLastTwoMoves(board)
            continue
        elif command.lower() == '?':
            printCommandOptions()
            continue
        elif command.lower() == 'l':
            printAllLegalMoves(board, parser)
            continue
        elif command.lower() == 'r':
            move = getRandomMove(board, parser)
        elif command.lower() == 'exit' or command.lower() == 'quit':
            return
        try:
            move = parser.parse(command)
        except ValueError as error:
            print("%s" % error)
            continue
        makeMove(move, board)

board = Board()

def main():
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--two":
            twoPlayerGame(board)
        else:
            playerSide = askForPlayerSide()
            print()
            aiDepth = askForDepthOfAI()
            #opponentAI = AI(board, not playerSide, aiDepth)
            # Custom AI class
            opponentAI = CustomAI(board, not playerSide, aiDepth, TIME_LIMIT_SEC)
            startGame(board, playerSide, opponentAI)
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    main()
