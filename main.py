import pygame
import pygame_menu
import sys
import Board as b
import math
import AI

SQUARESIZE = 100
BLUE = (0, 165, 255)
RED = (255, 0 ,0)
BACKGROUND_COLOUR = (228, 230, 246)
YELLOW = (242, 230, 0)
COLUMN_COUNT = 7
ROW_COUNT = 6
GAME_OVER = False
PLAYER_ONE = 1
PLAYER_TWO = 2
GAME_SETTINGS = {"difficulty": 4, "isSinglePlayer": True}

pygame.init()

#-------------Set up screen settings--------------#

width = COLUMN_COUNT*SQUARESIZE
height = (ROW_COUNT+1)*SQUARESIZE
size = (width, height)
surface = pygame.display.set_mode(size)
myFont = pygame.font.SysFont("monospace", 75)


def changePlayer(currentPlayer):
    if currentPlayer == 1:
        currentPlayer = 2
    else:
        currentPlayer = 1
    return currentPlayer

def set_mode(value, mode):
    GAME_SETTINGS['isSinglePlayer'] = mode

def set_difficulty(value, difficulty):

    GAME_SETTINGS['difficulty'] = difficulty


def start_the_game():
    isSinglePlayer = GAME_SETTINGS['isSinglePlayer']
    currentPlayer = 1
    ai = AI.AI(PLAYER_ONE, PLAYER_TWO, GAME_SETTINGS['difficulty'])
    board = b.Board(COLUMN_COUNT, ROW_COUNT, SQUARESIZE)
    pygame.draw.rect(surface, BACKGROUND_COLOUR, (0, 0, width, SQUARESIZE))

    while not GAME_OVER:
        board.drawBoard(surface)
        pygame.display.update()

        #Tie game check and action
        if board.isFull():
            label = myFont.render("Tie game fools", 1, BLUE)
            pygame.draw.rect(surface, BACKGROUND_COLOUR, (0, 0, width, SQUARESIZE))
            surface.blit(label, (40, 10))
            board.drawBoard()
            pygame.display.update()
            pygame.time.wait(2000)
            gameover = True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # hovering chip animation
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(surface, BACKGROUND_COLOUR, (0, 0, width, SQUARESIZE))
                posx = event.pos[0];
                if currentPlayer == 1:
                    pygame.draw.circle(surface, RED, (posx, SQUARESIZE / 2), SQUARESIZE * 0.45)
                else:
                    pygame.draw.circle(surface, YELLOW, (posx, SQUARESIZE / 2), SQUARESIZE * 0.45)

            if event.type == pygame.MOUSEBUTTONDOWN:
                #players turn
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                if board.placeChip(col, currentPlayer):
                    if board.checkWinner(currentPlayer):
                        board.displayWinner(currentPlayer, surface)
                        sys.exit()
                    else:
                        currentPlayer = changePlayer(currentPlayer)

                #AI's turn
                if isSinglePlayer:
                    col = ai.pickMove(board)
                    if board.placeChip(col, currentPlayer):
                        if board.checkWinner(currentPlayer):
                            board.displayWinner(currentPlayer, surface)
                            sys.exit()
                        else:
                            currentPlayer = changePlayer(currentPlayer)


#--------------start up menu ---------------#

menu = pygame_menu.Menu(width, height, 'Welcome to Connect 4', theme=pygame_menu.themes.THEME_BLUE)
menu.add_selector('Difficulty : ', [('Hard', 4), ('medium', 3), ('Easy', 2)], onchange=set_difficulty)
menu.add_selector('Mode : ', [('Singleplayer', True), ('Multiplayer', False)], onchange=set_mode)
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)
menu.mainloop(surface)