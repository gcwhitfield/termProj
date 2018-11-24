# George Whitfield 
# 15-112 Term Project 2018

import sys
import pygame
import wave
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
        self.song = 'ramune.wav'
        self.animationFrameTime = 1/60
        
        self.gameData = game.GameData(self, self.screen, self.song)
        self.songData = game.SongData(self)
        self.audioThread = self.gameData.musicThread

# define game variables
metaData = MetaData()

# start pygame
pygame.init()


#pygame.mixer.music.load('anote.wav')
#pygame.mixer.music.play(-1)


def drawMainMenu(screen, data):
    data.mainMenu.run(screen)

def drawGame(screen, data):
    data.gameData.runGame()

def drawDisplay(                                                                                        screen, data):
    if data.gameState == 'menu':
        drawMainMenu(screen, data)
    elif data.gameState == 'game':
        drawGame(screen, data)

colo = colors.Colors()
while 1: # run the pygame window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            metaData.audioThread.join()
            sys.exit()
    metaData.screen.fill((0, 0, 0))
    cursorPos = pygame.mouse.get_pos()
    drawDisplay(metaData.screen, metaData)

    rect = pygame.Rect(cursorPos, (50, 50))
    pygame.draw.rect(metaData.screen, colo.GREEN, rect, 0)
    pygame.display.flip()
