# George Whitfield
# 15-112 Term Project 2018
# The data and logic for the main menu

import sys
from button import MainMenuButton, StartLevelButton, SongSelectButton
from colors import Colors
import pygame
import os

class SongSelectButtonsGroup:
    # create a list of buttons based on the songs in our Music directory
    def createButtonObjectsFromFilePaths(self):
        buttonObjectLst = []
        for path in self.buttonsFilePaths:
            buttonObjectLst.append(SongSelectButton(0, 0, 
            self.metaData.width, self.buttonHeight,
            self.backgroundColor,
            self.metaData,
            path
            ))
        return buttonObjectLst

    def __init__(self, metaData, buttonFilePaths, buttonHeight):
        self.metaData = metaData
        self.buttonHeight = buttonHeight
        self.backgroundColor = Colors().BLACK
        self.buttonsFilePaths = buttonFilePaths
        self.buttonObjects = self.createButtonObjectsFromFilePaths()
        self.buttonsPerScreen = ((self.metaData.height - 200) // self.buttonHeight) - 1
        self.currentScreen = 0
        self.numberOfScreens = len(self.buttonObjects) // self.buttonsPerScreen

    # handle song selection button mouse cick
    def mouseClicked(self, mousePos, buttonsOnScreen):
        for button in buttonsOnScreen:
            if button.isClicked(mousePos):
                button.onClick()

    # draw the buttons and check to see if the buttons are clicked
    # I'm violating the principles of model, view, controller so that I can easily check clicks
    def draw(self, screen):
        buttonsOnScreen = set()
        for i in range(self.buttonsPerScreen):
            buttonIndex = i + (self.numberOfScreens * self.currentScreen)
            if buttonIndex < len(self.buttonObjects):
                currButton = self.buttonObjects[buttonIndex]
                currButton.posy = 200 + (i * self.buttonHeight)
                currButton.draw(screen)
                buttonsOnScreen.add(currButton)
        if pygame.mouse.get_pressed()[0]: # get left click
            mousePos = pygame.mouse.get_pos()
            self.mouseClicked(mousePos, buttonsOnScreen)


# contains the data for the main Menu
class MainMenu:
    # initalize the list of song filepaths
    def initButtons(self):
        buttonLst = []
        musicFolder = self.metaData.songsFolder
        buttons = os.listdir(musicFolder)
        for song in buttons:
            if '.DS_Store' not in song: # ignore the store file
                buttonLst.append(song)
        return buttonLst

    def __init__(self, metaData, screen):
        self.metaData = metaData
        self.screen = screen
        self.currScreen = 'mainMenu'
        self.screens = (
            'mainMenu',
            'options',
            'fileSelect',
            'play'
        )
        self.backgroundColor = (0, 0, 0) # rgb values
        self.beatDownImagePath = 'ImageAssets/beatdown.png'
        self.mainMenuButtonSpacing = 100

        self.songSelectButtons = SongSelectButtonsGroup(
            self.metaData, 
            self.initButtons(), # the list of button filePaths
            100) # height of each button
        
        self.mainMenuButtons = set([
            MainMenuButton(self.metaData.width//2, self.metaData.height//2, # position
            100, 50, # size
            'PLAY', # text
            self.backgroundColor, # background color
            'play', # click destination
            self.metaData, # MainMenu
            txtColor = Colors().WHITE), # text color

            MainMenuButton(self.metaData.width//2,
            self.metaData.height//2 + self.mainMenuButtonSpacing,
            100, 50,
            'OPTIONS',
            self.backgroundColor,
            'options',
            self.metaData,
            txtColor = Colors().WHITE),

            MainMenuButton(self.metaData.width//2,
            self.metaData.height//2 + 2*self.mainMenuButtonSpacing,
            100, 50,
            'QUIT',
            self.backgroundColor,
            'quit',
            self.metaData,
            txtColor = Colors().WHITE) # exit the game if button clicked
        ]),
        self.optionsButtons = set([
            MainMenuButton(100, 100,
            100, 50,
            'BACK',
            self.backgroundColor,
            'mainMenu',
            self.metaData,
            txtColor = Colors().WHITE),
        ]),
        self.playButtons = set([
            MainMenuButton(100, 100,
            100, 50,
            'BACK',
            self.backgroundColor,
            'mainMenu',
            self.metaData,
            txtColor = Colors().WHITE),

            StartLevelButton(self.metaData.width//2, 100,
            100, 50,
            'START',
            self.backgroundColor,
            'game',
            self.metaData,
            txtColor = Colors().WHITE),
        ]),

    def drawBackGround(self, screen):
        screen.fill(self.backgroundColor)
    
    def drawBeatDownImage(self, screen):
        image = pygame.image.load(self.beatDownImagePath)
        rect = image.get_rect()
        rect.centerx = self.metaData.width // 2
        rect.centery = self.metaData.height // 2 - 150
        screen.blit(image, rect)
    
    def drawMainMenu(self, screen):
        for tup in self.mainMenuButtons:
            for button in tup:
                button.draw(screen)
        self.drawBeatDownImage(screen)

    def drawOptionsScreen(self, screen):
        for tup in self.optionsButtons:
            for button in tup:
                button.draw(screen)
            
    def drawFileSelect(self, screen):
        pass

    def drawSongSelectButtons(self, screen):
        self.songSelectButtons.draw(screen)

    def drawPlayScreen(self, screen):
        for tup in self.playButtons:
            for button in tup:
                button.draw(screen)

        self.drawSongSelectButtons(screen)
    def draw(self, screen):
        self.drawBackGround(screen)
        if self.currScreen == 'mainMenu':
            self.drawMainMenu(screen)
        elif self.currScreen == 'options':
            self.drawOptionsScreen(screen)
        elif self.currScreen == 'fileSelect':
            self.drawFileSelect(screen)
        elif self.currScreen == 'play':
            self.drawPlayScreen(screen)

    def changeScreen(self, targetScreen):
        if targetScreen in self.screens:
            self.currScreen = targetScreen

    def getButtons(self):
        if self.currScreen == 'mainMenu':
            return self.mainMenuButtons
        elif self.currScreen == 'options':
            return self.optionsButtons
        elif self.currScreen == 'play':
            return self.playButtons

    def mouseClicked(self, mousePos): # check if clicked on button
        for tup in self.getButtons():
            for button in tup:
                if button.isClicked(mousePos):
                    button.onClick()

    def run(self, screen):
        self.draw(screen)
        if pygame.mouse.get_pressed()[0]: # get left click
            mousePos = pygame.mouse.get_pos()
            self.mouseClicked(mousePos)
