# George Whitfield
# 15-112 Term Project 2018

import sys
from button import MainMenuButton, StartLevelButton
from colors import Colors
import pygame
# contains the data for the main Menu
class MainMenu:
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

        self.mainMenuButtonSpacing = 100
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

    def drawMainMenu(self, screen):
        for tup in self.mainMenuButtons:
            for button in tup:
                button.draw(screen)

    def drawOptionsScreen(self, screen):
        for tup in self.optionsButtons:
            for button in tup:
                button.draw(screen)
            
    def drawFileSelect(self, screen):
        pass

    def drawPlayScreen(self, screen):
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
