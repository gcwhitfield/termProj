# George Whitfield
# 15-112 Term Project 2018
# The data and logic for the main menu

import sys
from button import *
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
        self.buttonsPerScreen = ((self.metaData.height - 200) // self.buttonHeight)
        self.currentScreen = 0
        self.numberOfScreens = (len(self.buttonObjects) // self.buttonsPerScreen) + 1

    # handle song selection button mouse cick
    def mouseClicked(self, mousePos, buttonsOnScreen):
        for button in buttonsOnScreen:
            if button.isClicked(mousePos):
                button.onClick()

    # draw the buttons and check to see if the buttons are clicked
    # I'm violating the principles of model, view, controller so that I can easily check clicks
    def draw(self, screen):
        buttonsOnScreen = set()
        leftMarginWidth = 150
        for i in range(self.buttonsPerScreen):
            buttonIndex = i + (self.buttonsPerScreen * self.currentScreen)
            if buttonIndex < len(self.buttonObjects):
                currButton = self.buttonObjects[buttonIndex]
                currButton.posy = 200 + (i * self.buttonHeight)
                currButton.posx = leftMarginWidth
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
        # metaData and pygame 
        self.metaData = metaData
        self.screen = screen
        self.currScreen = 'mainMenu'
        self.screens = (
            'mainMenu',
            'options',
            'fileSelect',
            'play'
        )
        # background color of menu
        self.backgroundColor = (0, 0, 0) # rgb values

        # path to the beatDown logo
        self.beatDownImagePath = 'ImageAssets/beatdown.png'
        self.mainMenuButtonSpacing = 100

        # if this variable is true, then we will display the notice that a song does not
        # have frequency data loaded into the game.
        self.displaySongLoadNotice = False

        # song select buttons
        self.songSelectButtons = SongSelectButtonsGroup(
            self.metaData, 
            self.initButtons(), # the list of button filePaths
            100) # height of each button
        
        # the buttns displayed on the main menu
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
        # buttons on the options screen
        self.optionsButtons = set([
            MainMenuButton(50, 50,
            100, 50,
            'BACK',
            self.backgroundColor,
            'mainMenu',
            self.metaData,
            txtColor = Colors().WHITE),
        ]),
        # buttons on the play screen
        self.playButtons = set([
            MainMenuButton(100, 50,
            100, 50,
            'BACK',
            self.backgroundColor,
            'mainMenu',
            self.metaData,
            txtColor = Colors().WHITE),

            StartLevelButton(self.metaData.width//2, 50,
            100, 50,
            'START',
            self.backgroundColor,
            'game',
            self.metaData,
            txtColor = Colors().WHITE,
            checkIfSongLoaded=True),

            SongPageScrollButton(50, 150,
            100, 100,
            self.metaData,
            direction=1),
            
            SongPageScrollButton(50, self.metaData.height - 50,
            100, 100,
            self.metaData,
            direction=-1)
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

    def drawSongLoadNotice(self, screen):
        # draw black background
        backGroundColor = (0, 0, 0) 
        backGroundRect = pygame.Rect(0, 
                                  0, 
                                  self.metaData.width, 
                                  self.metaData.height)
        pygame.draw.rect(screen, backGroundColor, backGroundRect, 0)

        # draw the text
        fontSize = 40
        fontColor = Colors().WHITE
        textx = self.metaData.width//2
        texty = 100
        text = '''\
You have selected a song that is
currently not loaded into BeatDown.

If you click "Okay", BeatDown will
process the selected song, save it
to a file, and then run the game. Saving
the song to a file can take up to
five minutes dependin on the length
of the song.

You only need to process the song once.
'''
        lineCount = 0
        for line in text.splitlines():
            lineCount += 1 # loop through the lines of our message and display them
            txtData = pygame.font.SysFont(None,
                                    fontSize) # font size
            # i learned the logic for displaying texts in pygame from this wordpress
            # website
            # https://sivasantosh.wordpress.com/2012/07/18/displaying-text-in-pygame/
            lineText = txtData.render(line, True, fontColor, backGroundColor)
            rect = lineText.get_rect()
            rect.centerx = textx
            rect.centery = texty + fontSize * lineCount
            screen.blit(lineText, rect)

        # create the "Okay" button
        okayButton = StartLevelButton(
            self.metaData.width//4, # position x
            self.metaData.height - 100, # position y
            100, # width
            50, # height
            'Okay', # text
            Colors().BLACK, # background color
            'game', # target screen
            self.metaData,
            txtColor = Colors().WHITE,
            checkIfSongLoaded=False)
        okayButton.draw(screen) # draw the button
        if okayButton.isClicked(pygame.mouse.get_pos()): # if the button is clicked
            okayButton.onClick() # execute click behavior
        
        # create the "Nope" button
        nopeButton = MainMenuButton((self.metaData.width//4) * 3, self.metaData.height - 100, # position
            100, 50, # size (width, height)
            'Nope', # display text
            self.backgroundColor,
            'play',
            self.metaData,
            txtColor = Colors().WHITE)
        nopeButton.draw(screen)
        if nopeButton.isClicked(pygame.mouse.get_pos()): # if the button is clicked
            nopeButton.onClick() # execute click behavior

    def drawFileSelect(self, screen):
        self.drawSongSelectButtons(screen)
        # if the song display notice is true, then display the notice
        if self.displaySongLoadNotice:
            self.drawSongLoadNotice(screen)

    def drawSongSelectButtons(self, screen):
        self.songSelectButtons.draw(screen)

    def drawPlayScreen(self, screen):
        self.drawFileSelect(screen)
        for tup in self.playButtons:
                for button in tup:
                    button.draw(screen)
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