# George Whitfield
# 15-112 Term Project 2018

#import playAudio
import pygame
import wave

import pyaudio
import wavInterpretation


class GameData:
    def __init__(self, metaData, screen, song):
        self.chunkSize = 2205 # 1/20 of a second
        self.gameTime = -1
        self.metaData = metaData
        self.screen = screen
        self.song = song
        self.songObject = wavInterpretation.WavFile(self.song, self.chunkSize)
        self.currentBeat = 0
        self.isPaused = False
        self.pauseScreen = 0

        self.enemies = set()

        self.audioStarted = False
        self.backgroundColor = (50, 0, 0)
        
        self.wf = wave.open(self.song, 'rb')
        self.audioData = self.wf.readframes(self.chunkSize)
        self.p = pyaudio.PyAudio()
        # open stream based on the wave object which has been input.
        self.stream = self.p.open(format =
                self.p.get_format_from_width(self.wf.getsampwidth()),
                channels = self.wf.getnchannels(),
                rate = self.wf.getframerate(),
                output = True)

        self.songLoudnessData = self.songObject.loudnessPerChunk
        self.maxLoudness = self.songObject.maxLoudness
        self.averageLoudness = self.songObject.averageLoudness
    
    def drawBackground(self, screen):
        screen.fill(self.backgroundColor)

    def drawGameScreen(self, screen):
        self.drawBackground(screen)

        rectWidth = 10 + (200 * (self.songLoudnessData[self.gameTime] / (self.averageLoudness * 1.75)))
        rect = pygame.Rect(self.metaData.width//2, self.metaData.height//2, rectWidth, 50)
        pygame.draw.rect(screen, (100, 100, 100), rect, 0)

        # draw a box for testing
    def drawEnemies(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
    
    def playAudio(self):
        self.stream.write(self.audioData)
        self.audioData = self.wf.readframes(self.chunkSize)

    def runGame(self):
        self.gameTime += 1
        self.playAudio()
        self.drawGameScreen(self.screen)
       
        #print(self.gameTime)

        
    def isOnBeat(self, frameData):
        pass

    def beatFired(self):
        pass

    # RUNS EVERY 1/60 OF A SECOND
    def timerFired(self, frameData): # playAudio will call timerFired
        self.isOnBeat(frameData)
        self.drawGameScreen(self.screen)
        print(self.gameTime)