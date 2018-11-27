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
        self.width = 1200
        self.height = 800
        self.chunkSize = 735
        self.screen = pygame.display.set_mode(
            [
                self.width, # x size of the screen
                self.height  # y size of the screen
            ]
        )
        self.mainMenu = mainMenu.MainMenu(self, self.screen)
        self.currScreen = 'menu'
        self.screens = (
            'menu',
            'game',
        )
        self.brightness = 50 # out of a max of 100
        
        self.song = 'notestest2.wav'
        self.animationFrameTime = 1/60
        

        self.emptyGameData = game.GameData
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

def drawDisplay(screen, data):
    if data.currScreen == 'menu':
        drawMainMenu(screen, data)
    elif data.currScreen == 'game':
        drawGame(screen, data)

colo = colors.Colors()
while 1: # run the pygame window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            metaData.audioThread.join()
            sys.exit()
    metaData.screen.fill((0, 0, 0))

    drawDisplay(metaData.screen, metaData)
    pygame.display.flip()
