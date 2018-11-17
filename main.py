# George Whitfield 
# 15-112 Term Project 2018

import sys
import pygame

# game classes
from mainMenu import *
from game import *

class MetaData:
    def __init__(self):
        self.gameState = 'menu'
        self.possibleGameStates = (
            'menu',
            'play'
        )
        self.game
        self.brightness = 50 # out of a max of 100
        self.mainMenuData = mainMenu.MenuData(self)
        self.gameData = game.GameData(self)

        self.width = 500
        self.height = 500

def drawMainMenu(screen, data):
    mainMenu.draw(screen, MenuData)

def drawGame(screen, data):
    pass
    
pygame.init()
size = width, height = 320, 820
speed = [1, 3]
black = 0, 0, 0

screen = pygame.display.set_mode(size)


size = (30, 30)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)
    pygame.draw.rect(screen, (100, 100, 100), boxrect, 0)
    pygame.display.flip()