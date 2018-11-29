# George Whitfield
# 15-112 Term Project 2018
# This file runs the 'game' mode where the user listens to the song and plays the level

import pygame
import wave
from wavInterpretation import WavFile
import threading
import threadPlayAudio
import threading
from enemies import *
from player import Player
from button import EndLevelButton
from colors import Colors

class SongData:
    def __init__(self, metaData):
        self.metaData = metaData
        self.chunkTimer = 0
        self.chunkCount = 0

class GameData:
    def __init__(self, metaData, screen, song):
        self.currScreen = 'game' # screen is either game or endLevel
        self.colors = Colors()
        self.metaData = metaData
        self.initialized = True
        self.chunkSize = self.metaData.chunkSize # 1/60 of a second
        self.gameTime = -1
        self.screen = screen
        self.song = song
        self.songObject = WavFile(self.song, self.chunkSize)
        self.currentBeat = 0
        self.isPaused = False
        self.pauseScreen = 0
        self.backgroundColor = (0, 0, 0)

        # player 
        self.player = Player(self.metaData)

        # set of enemies on screen
        self.enemies = set() 
        self.enemiesToRemove = set()
        self.bulletsToAdd = set()

        # coins data
        self.coins = set()
        self.coinsToRemove = set()
        self.coinSpawnFrequency = 60 # the number of animation frames in between each coin spawn
        self.score = 0
        self.maxScore = 0
        self.COIN_DRAW_LOCK = False # make sure we don't draw to draw and remove coins at the same time
        
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

        self.lengthOfIntensityIntervalInSeconds = 5 # five seconds
        # the number of samples in one intensity interval
        self.intensityInterval = self.songObject.sampleRate * self.lengthOfIntensityIntervalInSeconds 

        self.intensityData = self.songObject.calcIntensityForWholeSong(self.intensityInterval)
        self.currIntensityInterval = 0
        
        # enemy data
        # a lower enemy spawn frequency corresponds to a HIGHER spawn rate
        self.enemySpawnFrequency = 60 # spawn every second
        self.ENEMY_DRAW_LOCK = False # lock on drawing enemies and removing them
        self.enemySpawnRates = {
            'box': 1,
            'spinny': 5
        }
                
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

    def mouseClicked(self, mousePos, buttons): # check if clicked on button
            for button in buttons:
                if button.isClicked(mousePos):
                    button.onClick()
        
    def drawGameScreen(self, screen):
        if self.currScreen == 'game':
            self.drawBackground(screen)
            self.displayAudioSpectrumBackground(screen)

            self.coinBehavior()
            self.enemyBehavior()

            self.player.draw()
        elif self.currScreen == 'endLevel':
            self.drawEndLevelScreen(screen)

    def drawEndLevelScreen(self, screen):
        cursorPos = pygame.mouse.get_pos()
        # draw the text
        txtData = pygame.font.SysFont(None,
                                self.metaData.height//10) # font size
        # i learned the logic for displaying texts in pygame from this wordpress
        # website
        # https://sivasantosh.wordpress.com/2012/07/18/displaying-text-in-pygame/
        scoreText = txtData.render(
            'Score : ' + str(self.score),
             True,
             self.colors.WHITE, 
             self.backgroundColor)
        rect = scoreText.get_rect()
        rect.centerx = self.metaData.width//2
        rect.centery = self.metaData.width//2 - 300
        screen.blit(scoreText, rect)
        # buttons
        endLevelButtons = set([
            EndLevelButton(self.metaData.width//2, self.metaData.height//2,
            200, 50,
            'MAIN MENU',
            self.backgroundColor,
            'menu',
            self.metaData,
            txtColor = Colors().WHITE)
         ])
        # draw the buttons and handle the click behavior
        for button in endLevelButtons:
            button.draw(screen)
            if pygame.mouse.get_pressed()[0]: # get left click
                if button.isClicked(cursorPos):
                    button.onClick()
    
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
        if frameData > self.averageLoudness * 2:
            return True
        else:
            return False

    def beatFired(self): # beatMove the enemies
        for enemy in self.enemies:
            enemy.beatMove()

    def nonBeatFired(self):
        self.moveEnemies()

    def spawnEnemiesBasedOnInensity(self):
        inten = self.intensityData[self.currIntensityInterval]
        if inten < 0.25:
            self.enemySpawnFrequency = 1000
        elif inten < 0.5:
            self.enemySpawnFrequency = 700
        elif inten < 0.75:
            self.enemySpawnFrequency = 300
        else:
            self.enemySpawnFrequency = 2000
    
    # add an enemy in the game based off of the intensity
    def addEnemy(self):
        currIntensity = self.intensityData[self.currIntensityInterval]
        enemy = 0
        if 0.7 < currIntensity < 1: # high intensity
            enemy = ShootySpinnyEnemy(self.metaData)
        elif 0.5 < currIntensity < 0.7: # medium intensity
            enemy = ShootySpinnyEnemy(self.metaData)
        elif currIntensity < 0.5: # low intensity
            enemy = ShootySpinnyEnemy(self.metaData)
        
        self.enemies.add(enemy)

    def moveEnemies(self):
        for enemy in self.enemies:
            enemy.move()
            enemy.wallCollide()

    def enemyBehavior(self): # draw the enemies and handle the collisions
        self.ENEMY_DRAW_LOCK = True
        for enemy in self.enemies:
            enemy.draw()
            if enemy.isCollidingWithPlayer():
                self.score -= 2
                self.enemiesToRemove.add(enemy)
        self.ENEMY_DRAW_LOCK = False

    # remove all of the dead enemies
    def removeDeadEnemies(self):
        for enemy in self.enemiesToRemove:
            self.enemies.remove(enemy)
        self.enemiesToRemove = set()
    
    # remove all of the dead enemies
    def addBullets(self):
        # remove enemy from screen
        for bullet in self.bulletsToAdd:
            self.enemies.add(bullet)
        self.bulletsToAdd = set()

    # add a new coin to the screen
    def addCoin(self):
        self.coins.add(Coin(self.metaData))

    def removeDeadCoins(self):
        removeCoinsToRemove = set()
        # remove coins from the screen
        for coin in self.coinsToRemove:
            self.coins.remove(coin)
            removeCoinsToRemove.add(coin)
        # remove the coins from list of coins to remove
        for coin in removeCoinsToRemove:
            self.coinsToRemove.remove(coin)

    def coinBehavior(self): # draw the coins and handle the collisions
        self.COIN_DRAW_LOCK = True
        for coin in self.coins:
            coin.draw()
            # also handle the life drain of coins
            coin.lifeDrain()
            if coin.isCollidingWithPlayer():
                self.score += 1
                coin.life = 0
        self.COIN_DRAW_LOCK = False
    

    # RUNS EVERY 1/60 OF A SECOND
    def timerFired(self, frameData): # playAudio will call timerFired
        if self.gameTime >= len(self.songLoudnessData ) - 1: # if we are at the end of the song, then 
                # display the end level screen
                self.currScreen = 'endLevel'

        print(len(self.enemies))
        # while we are still in game mode
        if self.currScreen == 'game':
            self.gameTime += 1 # gameTime = current animation frame
            
            
            # only run this if we arent drawing enemies
            if not self.ENEMY_DRAW_LOCK: 
                self.removeDeadEnemies()
                self.addBullets() # handle shooting enemy behavior
            # only run if we arent drawing coins
            if not self.COIN_DRAW_LOCK:
                self.removeDeadCoins()

            # handle events on and off of the beat
            if self.isOnBeat():
                self.beatFired()
            else:
                self.nonBeatFired()

            # run every 5 seconds
            if (self.gameTime % 300) == 0: # update the intensity data 
                self.currIntensityInterval += 1
                print(self.intensityData[self.currIntensityInterval])
            
            
            if not self.ENEMY_DRAW_LOCK:
                if self.gameTime % self.enemySpawnFrequency == 0: # add enemies
                    self.addEnemy()

            if not self.COIN_DRAW_LOCK:
                if self.gameTime % self.coinSpawnFrequency == 0:
                    self.addCoin()
            