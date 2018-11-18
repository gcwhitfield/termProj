# George Whitfield 
# 15-112 Term Project 2018

import sys
import pygame

# game classes
import mainMenu
import game


# start pygame
pygame.init()

#pygame.mixer.music.load('anote.wav')
#pygame.mixer.music.play(-1)

class MetaData:
    def __init__(self):
        self.width = 800
        self.height = 800
        self.screen = pygame.display.set_mode(
            [
                self.width, # x size of the screen
                self.height  # y size of the screen
            ]
        )
        self.gameState = 'game'
        self.possibleGameStates = (
            'menu',
            'game',
        )
        self.brightness = 50 # out of a max of 100
        self.mainMenu = mainMenu.MainMenu(self, self.screen)
        self.gameData = game.GameData(self, self.screen, 'notesTest3.wav')

def drawMainMenu(screen, data):
    data.mainMenu.run(screen)

def drawGame(screen, data):
    data.gameData.runGame()

def drawDisplay(screen, data):
    if data.gameState == 'menu':
        drawMainMenu(screen, data)
    elif data.gameState == 'game':
        drawGame(screen, data)

# define game variables
size = width, height = 600, 600
speed = [1, 3]
black = 0, 0, 0
metaData = MetaData()

import time


size = (30, 30)
while 1: # run the pygame window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    time1 = time.time()
    metaData.screen.fill((0, 0, 0))
    cursorPos = pygame.mouse.get_pos()
    drawDisplay(metaData.screen, metaData)

    rect = pygame.Rect(cursorPos, (50, 50))
    pygame.draw.rect(metaData.screen, (100, 100, 100), rect, 0)
    pygame.display.flip()
    print(time.time() - time1)