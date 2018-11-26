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
        self.chunkCount = 0

class GameData:
    def __init__(self, metaData, screen, song):
        self.chunkSize = 1460 # 1/20 of a second
        self.gameTime = -1
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

        self.backgroundColor = (0, 0, 0)
        
        # initialize the music
        self.musicThread = threading.Thread(target = threadPlayAudio.run, args = (self,))
        self.audioStarted = False

        # music data
        self.songLoudnessData = self.songObject.loudnessPerChunk
        self.maxLoudness = self.songObject.maxLoudness
        self.averageLoudness = self.songObject.averageLoudness
        self.songObject.configureSpectrumData()
        self.musicSpectrums = self.songObject.frequencySpectrumData
        self.lowsMidsHighsValues = self.songObject.lowsMidsHighsSpectrum(self.musicSpectrums)

        self.intensityInterval = self.songObject.sampleRate * 10 # five seconds
        self.intensityData = self.songObject.calcIntensityForWholeSong(self.intensityInterval)
        self.currIntensityInterval = 0

    def drawBackground(self, screen):
        screen.fill(self.backgroundColor)

    def displayAudioSpectrumBackground(self, screen):
        rectBorder = 5
        currSpectrum = self.musicSpectrums[self.gameTime]
        gameWidth = self.metaData.width
        gameHeight = self.metaData.height
        rectWidth = gameWidth / len(currSpectrum)
        posy = 0
        
        for index in range(len(currSpectrum)):
            dataPoint = currSpectrum[index]
            height = dataPoint//100
            rect = pygame.Rect
            posx = index * rectWidth
            rect = pygame.Rect(posx, posy, rectWidth - rectBorder, height)
            pygame.draw.rect(screen, (100, 0, 100), rect, 0)

    def drawGameScreen(self, screen):
        self.drawBackground(screen)
        self.displayAudioSpectrumBackground(screen)

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
            return True
        else:
            return False

    def beatFired(self):
        for enemy in self.enemies:
            enemy.beatMove()

    # RUNS EVERY 1/60 OF A SECOND
    def timerFired(self, frameData): # playAudio will call timerFired
        self.gameTime += 1
        if self.isOnBeat():
            self.beatFired()
        for enemy in self.enemies:
            enemy.move()
            enemy.isCollidingWithWall()
        if (self.gameTime % 600) == 0:
            self.currIntensityInterval += 1
            print(self.intensityData[self.currIntensityInterval])