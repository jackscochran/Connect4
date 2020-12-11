#board rating system
#center column: +4
#lines of two: +2
#lines of three: +5
#4 in a row: +100000000
#opp line of two: -2
#opp winnable line of three: -100
import copy
import random
import math

class AI:

    def __init__(self, playerNumber, oppNumber, diff):
        self.piece = playerNumber
        self.opponent = oppNumber
        self.difficulty = diff

    def scoreWindow(self, window):
        score = 0
        if window.count(self.piece) == 4:
            score += 1000
        if window.count(self.piece) == 3 and window.count(0) == 1:
            score += 15
        if window.count(self.piece) == 2 and window.count(0) == 2:
            score += 5
        if window.count(self.opponent) == 3 and window.count(0) == 1:
            score -= 700
        if window.count(self.opponent) == 2 and window.count(0) == 2:
            score -= 3

        return score

    def boardScore(self, board):
        score = 0
        #horizontal check
        for row in range(board.shape[1]):
            for col in range(board.shape[0]-3):
                window = [board[col][row], board[col+1][row], board[col+2][row], board[col+3][row]]
                score += self.scoreWindow(window)

        #vertical check
        for col in board:
            for row in range(board.shape[1] - 3):
                window = [col[row], col[row + 1], col[row + 2], col[row + 3]]
                score += self.scoreWindow(window)

        #diagonal check
        for col in range(board.shape[0]-3):
            for row in range(board.shape[1]-3):
                window = [board[col][row], board[col+1][row+1], board[col+2][row+2], board[col+2][row+2]]
                score += self.scoreWindow(window)
                window = [board[col][row+3], board[col+1][row+2]], board[col+2][row+1], board[col+3][row]
                score += self.scoreWindow(window)

        #middle check
        for row in board[3]:
            if row == self.piece:
                score += 3
        return score


    def isTerminalNode(self, boardObject):
        return boardObject.checkWinner(self.piece) or boardObject.checkWinner(self.opponent) or boardObject.isFull()

    def minimax(self, boardObject, depth, maximizingPlayer):
        validLocations = boardObject.validLocations()
        bestMove = random.choice(validLocations)

        if depth == 0 or self.isTerminalNode(boardObject):
            if boardObject.checkWinner(self.piece):
                return None, 100000000
            elif boardObject.checkWinner(self.opponent):
                return None, -100000000
            elif boardObject.isFull(): # tie game
                return None, 0
            else:
                return None, self.boardScore(boardObject.board)

        if maximizingPlayer:
            currentScore = -math.inf
            for location in validLocations:
                tempBoard = copy.deepcopy(boardObject)
                tempBoard.placeChip(location, self.piece)
                newScore = self.minimax(tempBoard, depth - 1, False)[1]
                if newScore > currentScore:
                    currentScore = newScore
                    bestMove = location

            return bestMove, currentScore

        else:
            currentScore = math.inf
            for location in validLocations:
                tempBoard = copy.deepcopy(boardObject)
                tempBoard.placeChip(location, self.opponent)
                newScore = self.minimax(tempBoard, depth - 1, True)[1]
                if newScore < currentScore:
                    currentScore = newScore
                    bestMove = location

            return bestMove, currentScore

    def pickMove(self, boardObject):
        return self.minimax(boardObject, self.difficulty, True)[0]

