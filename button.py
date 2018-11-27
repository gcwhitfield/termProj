# George Whitfield 
# 15-112 Term Project

import pygame
import sys

class Button:
    def __init__(self, posx, posy, width, height, text, backGroundColor, 
                onClickEvent = None, border = 0, txtColor = None):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.text = text
        self.backGroundColor = backGroundColor

        self.defaultColor = (109, 232, 102)
        self.button = pygame.Rect(self.posx - self.width//2, 
                                  self.posy - self.height//2, 
                                  self.width, 
                                  self.height)
    
        self.border = border

        if onClickEvent != None:
            self.onClickEvent = onClickEvent
        
        if txtColor == None:
            self.txtColor = (0, 0, 0) # default to black
        else:
            self.txtColor = txtColor

    def drawText(self, screen):
        pygame.font.init()
        txtData = pygame.font.SysFont(None,
                                self.height) # font size
        # i learned the logic for displaying texts in pygame from this wordpress
        # website
        # https://sivasantosh.wordpress.com/2012/07/18/displaying-text-in-pygame/

        text = txtData.render(self.text, True, self.txtColor, self.backGroundColor)
        rect = text.get_rect()
        rect.centerx = self.posx
        rect.centery = self.posy
        screen.blit(text, rect)

    def draw(self, screen):
        pygame.draw.rect(screen, self.backGroundColor, self.button, self.border)
        self.drawText(screen)

class MainMenuButton(Button):
    def __init__(self, posx, posy, width, height, text, backGroundColor, targetScreen, metaData,
                onClickEvent=None, border=0, txtColor=None):
        super().__init__(posx, posy, width, height, text, backGroundColor, onClickEvent=onClickEvent, border=border, txtColor=txtColor)
        self.targetScreen = targetScreen
        self.metaData = metaData

    def isClicked(self, mousePosition):
        # mouse position is an (x, y) tuple
        x, y = mousePosition
        if self.posx - self.width//2 < x and self.posx + self.width//2 > x and \
        self.posy - self.height//2 < y and self.posy + self.height//2 > y:
            self.onClick()
    
    def onClick(self): # when the button gets clicked, execute the code
        print('buttonClicked')
        print(self.metaData)
        if self.targetScreen == 'menu':
            # initialize the gameData every time we click on this button
            self.metaData.gameData = self.metaData.emptyGameData(self.metaData, self.metaData.screen, self.metaData.song)
        elif self.targetScreen in self.metaData.mainMenu.screens:
            self.metaData.mainMenu.currScreen = self.targetScreen 
        elif self.targetScreen == 'quit':
            sys.exit()

class EndLevelButton(MainMenuButton):
    def __init__(self, posx, posy, width, height, text, backGroundColor, targetScreen, metaData, onClickEvent=None, border=0, txtColor=None):
        super().__init__(posx, posy, width, height, text, backGroundColor, targetScreen, metaData, onClickEvent=onClickEvent, border=border, txtColor=txtColor)

    def onClick(self): # when the button gets clicked, execute the code
        print('buttonClicked')
        print(self.metaData)
        if self.targetScreen == 'menu':
            # initialize the game every time we click on this button
            self.metaData.__init__()

class StartLevelButton(MainMenuButton):
    def __init__(self, posx, posy, width, height, text, backGroundColor, targetScreen, metaData, onClickEvent=None, border=0, txtColor=None):
        super().__init__(posx, posy, width, height, text, backGroundColor, targetScreen, metaData, onClickEvent=onClickEvent, border=border, txtColor=txtColor)

    def onClick(self): # when the button gets clicked, execute the code
        print('buttonClicked')
        print(self.metaData)
        if self.targetScreen == 'game':
            # initialize the gameData every time we click on this button
            self.metaData.currScreen = 'game'