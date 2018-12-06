# George Whitfield 
# 15-112 Term Project 2018
# Run the game

import sys
import pygame
import wave
import os

# game classes
import mainMenu
import game
from wavInterpretation import WavFile
import time

import threadPlayAudio
import threading

import colors

class MetaData:
    def __init__(self):
        self.CLOSE_GAME = False
        self.width = 1200
        self.height = 800
        self.chunkSize = 735
        self.screen = pygame.display.set_mode(
            [
                self.width, # x size of the screen
                self.height  # y size of the screen
            ]
        )
        self.currScreen = 'menu'
        self.screens = (
            'menu',
            'game',
        )
        self.brightness = 50 # out of a max of 100
        
        self.songsFolder = 'Music/'
        self.song = ''
        self.animationFrameTime = 1/60
        self.mainMenu = mainMenu.MainMenu(self, self.screen)

        self.emptyGameData = game.GameData
        # we need to define the gameData only when we have an acceptable file path
        if os.path.isfile(self.song):
            self.gameData = game.GameData(self, self.screen, self.song)
            self.audioThread = self.gameData.musicThread
        else:
            self.gameData = None

# define game variables
metaData = MetaData()

# start pygame
pygame.init()

def drawMainMenu(screen, data):
    data.mainMenu.run(screen)

def drawGame(screen, data):
    data.gameData.runGame()

def drawDisplay(screen, data):
    if data.currScreen == 'menu':
        drawMainMenu(screen, data)
    elif data.currScreen == 'game':
        drawGame(screen, data)

colo = colors.Colors()
while 1: # run the pygame window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            metaData.CLOSE_GAME = True
            if metaData.gameData != None:
                metaData.gameData.musicThread.join()
            sys.exit()
    metaData.screen.fill((0, 0, 0))

    drawDisplay(metaData.screen, metaData)
    pygame.display.flip()
