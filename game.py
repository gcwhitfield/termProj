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
from decorations import *
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
        #self.colors = Colors()
        self.metaData = metaData
        self.initialized = True
        self.chunkSize = self.metaData.chunkSize # 1/60 of a second
        self.gameTime = -1
        self.screen = screen # pygame screen
        self.song = song # song we are currently playing
        self.songObject = WavFile(self.song, self.chunkSize)
        self.currentBeat = 0 
        self.isPaused = False
        self.pauseScreen = 0
        self.backgroundColor = (0, 0, 0)
        # the main color will be used to determine the color of everything else
        self.mainColor = (0, 0, 0)

        # player 
        self.player = Player(self.metaData)

        # set of enemies on screen
        self.enemies = set() 
        self.enemiesToRemove = set()
        self.bulletsToAdd = set()
        self.currEnemy = BoxEnemy # which enemy we are currently spawning
        self.enemySpawnModifier = 1 # controls how often the enemies spawn

        # coins data
        self.coins = set()
        self.coinsToRemove = set()
        self.coinSpawnFrequency = 60 # the number of animation frames in between each coin spawn
        self.score = 0
        self.maxScore = 0
        self.COIN_DRAW_LOCK = False # make sure we don't draw to draw and remove coins at the same time

        # decorations data
        self.numDecs = 200
        self.decorations = set()
        self.initalizeDecorations()
        self.decorationsToRemove = set()
        self.decorationsToAdd = set()
        self.DECORATIONS_LOCK = False

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
        self.numAnimationFramesPerIntenInterval = 300
        self.intensityData = self.songObject.calcIntensityForWholeSong(self.intensityInterval, self.songObject.lenInSamples)
        self.currIntensityInterval = 0

        # colors data
        self.colors = Colors()
        self.intensityColors = self.colors.calculateColorsForIntensityIntervals(self.intensityData)
        self.currMainColor = self.intensityColors[self.currIntensityInterval] # color for current interval
        self.colorLerp = 0 # update this every animatin frame and set back to zero every intensity interval
        self.instantColor = self.colors.calculateCurrentColor(self)
        print(self.intensityColors)
        # enemy data
        # a lower enemy spawn frequency corresponds to a HIGHER spawn rate
        self.enemySpawnFrequency = 60 # spawn every second
        self.ENEMY_DRAW_LOCK = False # lock on drawing enemies and removing them
        self.enemySpawnRates = {
            'box': 1,
            'spinny': 5
        }

    # run game. This gets called every PyGame frame
    def runGame(self):
        self.playAudio()
        self.drawGameScreen(self.screen)

    # draw background of the game 
    def drawBackground(self, screen):
        screen.fill(self.backgroundColor)

    # display the cool audio spectrum in the background
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

    # fire when the mouse is clicked
    def mouseClicked(self, mousePos, buttons): # check if clicked on button
            for button in buttons:
                if button.isClicked(mousePos):
                    button.onClick()
    
    # draw the stuff on the game screen
    def drawGameScreen(self, screen):
        if self.currScreen == 'game':
            self.drawBackground(screen)
            
            self.displayAudioSpectrumBackground(screen)
            self.decorationBehavior()
            self.coinBehavior()
            self.enemyBehavior()
            
            self.player.draw()
        elif self.currScreen == 'endLevel':
            self.drawEndLevelScreen(screen)

    # draw the end level screen
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

    # returns true if music is on the beat
    def isOnBeat(self):
        frameData = self.songLoudnessData[self.gameTime]
        if frameData > self.averageLoudness * 2:
            return True
        else:
            return False

    # fire when on the beat
    def beatFired(self): # beatMove the enemies
        for enemy in self.enemies:
            enemy.beatMove()
        self.beatMoveDecorations()
    # fire when not on the beat
    def nonBeatFired(self):
        self.moveEnemies()
        self.moveDecorations()

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
            enemy = BoxEnemy(self.metaData)
        elif 0.5 < currIntensity < 0.7: # medium intensity
            enemy = BoxEnemy(self.metaData)
        elif currIntensity < 0.5: # low intensity
            enemy = BoxEnemy(self.metaData)
        else:
            enemy = BoxEnemy(self.metaData)
        
        self.enemies.add(enemy)

    # when not on beat, move enemies normally. Also handle wall collisions
    def moveEnemies(self):
        for enemy in self.enemies:
            enemy.move()
            enemy.wallCollide()

    # draw the enemies and handle player collisions
    def enemyBehavior(self): # draw the enemies and handle the collisions
        self.ENEMY_DRAW_LOCK = True
        for enemy in self.enemies:
            enemy.draw()
            if enemy.isCollidingWithPlayer():
                self.score -= 2
                self.enemiesToRemove.add(enemy)
        self.ENEMY_DRAW_LOCK = False

    def intensityIntervalFired(self):
        self.currIntensityInterval += 1 # go to the next intensity interval
        self.currMainColor = self.intensityColors[self.currIntensityInterval]
        self.colorLerp = 0

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
    
    # decorations methods
    def initalizeDecorations(self):
        for dec in range(self.numDecs):
            self.decorations.add(Sparkle(self.metaData))
    # draw decs and handle collisions
    def decorationBehavior(self):
        self.DECORATIONS_LOCK = True
        for dec in self.decorations:
            dec.draw()
            dec.leaveScreenBehavior()
        self.DECORATIONS_LOCK = False
    
    def addNewDecorations(self):
        for dec in self.decorationsToAdd:
            self.decorations.add(dec)
        self.decorationsToAdd = set()

    # when non on beat, move deocorations normally
    def moveDecorations(self):
        for dec in self.decorations:
            dec.move()

    # move decorations on the beat
    def beatMoveDecorations(self):
        for dec in self.decorations:
            dec.beatMove()
    
    # remove the decorations that fall off of the screen
    def removeOldDecorations(self):
        for dec in self.decorationsToRemove:
            self.decorations.remove(dec)
        self.decorationsToRemove = set()

    # RUNS EVERY 1/60 OF A SECOND
    def timerFired(self, frameData): # playAudio will call timerFired
        if self.gameTime >= len(self.songLoudnessData ) - 1: # if we are at the end of the song, then 
                # display the end level screen
                self.currScreen = 'endLevel'
        # while we are still in game mode
        if self.currScreen == 'game':
            self.gameTime += 1 # gameTime = current animation frame
            
            # only run this if we arent drawing enemies
            if not self.ENEMY_DRAW_LOCK: 
                self.removeDeadEnemies()
                self.addBullets()
                if self.gameTime % self.enemySpawnFrequency == 0: # add enemies
                    self.addEnemy() # handle shooting enemy behavior
            # only run if we arent drawing coins
            if not self.COIN_DRAW_LOCK:
                self.removeDeadCoins()
                if self.gameTime % self.coinSpawnFrequency == 0:
                    self.addCoin()
            # only run when not drawing decorations
            if not self.DECORATIONS_LOCK:
                self.removeOldDecorations()
                self.addNewDecorations()
            # handle events on and off of the beat
            if self.isOnBeat():
                self.beatFired()
            else:
                self.nonBeatFired()

            # run every new intensity interval
            if (self.gameTime % self.numAnimationFramesPerIntenInterval) == 0: # update the intensity data 
                self.intensityIntervalFired()

            # update the color lerp
            self.colorLerp += 1
            # update instantanoues Color
            self.instantColor = self.colors.calculateCurrentColor(self)
            print(self.instantColor)