# George Whitfield
# 15-112 Term Project 2018

#import playAudio
import pygame
import wave
#import pyaudio

#import pyaudio
from wavInterpretation import WavFile
import threading

import threadPlayAudio
import threading

from enemies import *

class SongData:
    def __init__(self, metaData):
        self.metaData = metaData
        self.chunkTimer = 0
        self.chunkSize = 735 # 1/60 of a second of data
        self.chunkCount = -1

class GameData:
    def __init__(self, metaData, screen, song):
        self.chunkSize = 1460 # 1/20 of a second
        self.gameTime = 0
        self.metaData = metaData
        self.screen = screen
        self.song = song
        self.songObject = WavFile(self.song, self.chunkSize)
        self.currentBeat = 0
        self.isPaused = False
        self.pauseScreen = 0

        # set of enemies on screen
        self.enemies = set() 
        self.enemies.add(BoxEnemy(self.metaData))

        self.backgroundColor = (50, 0, 0)
        
        # initialize the music
        self.musicThread = threading.Thread(target = threadPlayAudio.run, args = (self,))
        self.audioStarted = False

        # music data
        self.songLoudnessData = self.songObject.loudnessPerChunk
        self.maxLoudness = self.songObject.maxLoudness
        self.averageLoudness = self.songObject.averageLoudness
    
    def drawBackground(self, screen):
        screen.fill(self.backgroundColor)

    def drawGameScreen(self, screen):
        self.drawBackground(screen)

        # draw a box for testing
        rectWidth = 10 + (200 * (self.songLoudnessData[self.gameTime] / (self.averageLoudness * 1.75)))
        rect = pygame.Rect(self.metaData.width//2, self.metaData.height//2, rectWidth, 50)
        pygame.draw.rect(screen, (100, 100, 100), rect, 0)

        self.drawEnemies(screen)

    def drawEnemies(self, screen):
        for enemy in self.enemies:
            enemy.draw()
    
    # execute the audio at the start of the level
    def playAudio(self):
        if self.audioStarted == False:
            self.audioStarted = True
            self.musicThread.start()

    def runGame(self):
        self.playAudio()
        self.drawGameScreen(self.screen)
    
    def isOnBeat(self):
        frameData = self.songLoudnessData[self.gameTime]
        if frameData > self.averageLoudness * 1.7:
            self.beatFired()
        else:
            pass

    def beatFired(self):
        for enemy in self.enemies:
            enemy.beatMove()



    # RUNS EVERY 1/60 OF A SECOND
    def timerFired(self, frameData): # playAudio will call timerFired
        self.gameTime += 1
        self.isOnBeat()
        for enemy in self.enemies:
            enemy.move()
            enemy.isCollidingWithWall()