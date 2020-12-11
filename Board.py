import numpy as np
import math
import pygame
BLUE = (3, 94, 216)
RED = (255, 0 ,0)
BACKGROUND_COLOUR = (228, 230, 246)
YELLOW = (242, 230, 0)


class Board:
    def __init__(self, columns, rows, squareSize):
        self.board = np.zeros((columns, rows))
        self.numOfCol = columns
        self.numOfRows = rows
        self.squareSize = squareSize

    def validLocations(self):
        validLocations = []
        for col in range(self.numOfCol):
            if self.board[col][0] == 0:
                validLocations.append(col)

        return validLocations

    def isValid(self, column, row):
        if column >= 0 and column < self.numOfCol and row >= 0 and row < self.numOfRows:
            return True

        return False

    def isFull(self):
        full = True
        for c in self.board:
            if c[0] == 0:
                full = False

        return full

    def placeChip(self, column, player):

        if self.board[column][0] != 0:
            print("this column is full")
            return False

        else:
            counter = 0
            for cell in self.board[column]:
                if cell == 0:
                    counter+= 1
                    continue
            self.board[column][counter-1] = player
            return True

    def checkWinner(self, player):
        #check horizontal
        for col in range(self.numOfCol-3):
            for row in range(self.numOfRows):
                if self.board[col][row] == player and self.board[col+1][row] == player and self.board[col+2][row] == player and self.board[col+3][row] == player:
                    return True

        #check vertical
        for col in range(self.numOfCol):
            for row in range(self.numOfRows-3):
                if self.board[col][row] == player and self.board[col][row+1] == player and self.board[col][row+2] == player and self.board[col][row+3] == player:
                    return True

        #check diagonal (towards top right)
        for c in range(self.numOfCol-3):
            for r in range(self.numOfRows-3):
                if self.board[c][r+3] == player and self.board[c+1][r+2] == player and self.board[c+2][r+1] == player and self.board[c+3][r] == player:
                    return True

        # check diagonal (towards top left)
        for c in range(self.numOfCol-3):
            for r in range(self.numOfRows-3):
                if self.board[c+3][r+3] == player and self.board[c+2][r+2] == player and self.board[c+1][r+1] == player and self.board[c][r] == player:
                    return True

        return False

    def printBoard(self):
        for i in range(6):
            for j in range(7):
                print(round(self.board[j][i]), end = "  ")
            print()

    def centerColumn(self):
        return math.ceil(self.numOfCol/2) - 1

    def drawBoard(self, screen):
        for c in range(self.numOfCol):
            for r in range(self.numOfRows):
                pygame.draw.rect(screen, BACKGROUND_COLOUR, (c * self.squareSize, self.squareSize + r * self.squareSize, self.squareSize, self.squareSize))
                pygame.draw.rect(screen, BLUE, (c * self.squareSize, self.squareSize + r * self.squareSize, self.squareSize, self.squareSize))
                pygame.draw.circle(screen, BACKGROUND_COLOUR,
                                   (c * self.squareSize + self.squareSize / 2, r * self.squareSize + self.squareSize * 3 / 2),
                                   self.squareSize * 0.44)

                if self.board[c, r] == 1:
                    pygame.draw.circle(screen, RED,
                                       (c * self.squareSize + self.squareSize / 2, r * self.squareSize + self.squareSize * 3 / 2),
                                       self.squareSize * 0.44)
                if self.board[c, r] == 2:
                    pygame.draw.circle(screen, YELLOW,
                                       (c * self.squareSize + self.squareSize / 2, r * self.squareSize + self.squareSize * 3 / 2),
                                       self.squareSize * 0.44)

    def displayWinner(self, player, surface):
        myFont = pygame.font.SysFont("monospace", 75)
        fontColor = BLUE

        label = myFont.render("Player " + str(player) + " wins!", 1, fontColor)
        pygame.draw.rect(surface, BACKGROUND_COLOUR, (0, 0, self.squareSize*self.numOfCol, self.squareSize))
        surface.blit(label, (40, 10))
        self.drawBoard(surface)
        pygame.display.update()
        pygame.time.wait(3000)
        gameover = True


