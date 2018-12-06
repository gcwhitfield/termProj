# George Whitfield 
# 15-112 Term Project
# Data about the buttons object use for the main menu

import pygame
import sys
import string
import os
import colors

class Button:
    def __init__(self, posx, posy, width, height, text=None, backGroundColor=(0, 0, 0), 
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
            self.txtColor = colors.Colors().WHITE # default to white
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
    def __init__(self, posx, posy, width, height, text='', backGroundColor=(0, 0, 0), \
    targetScreen=None, metaData=None,
                onClickEvent=None, border=0, txtColor=None):
        super().__init__(posx, posy, width, height, text, backGroundColor, onClickEvent=onClickEvent, \
        border=border, txtColor=txtColor)
        self.targetScreen = targetScreen
        self.metaData = metaData

    def isClicked(self, mousePosition):
        # mouse position is an (x, y) tuple
        x, y = mousePosition
        if self.posx - self.width//2 < x and self.posx + self.width//2 > x and \
        self.posy - self.height//2 < y and self.posy + self.height//2 > y:
            self.onClick()
    
    def onClick(self): # when the button gets clicked, execute the code
        if self.targetScreen == 'menu':
            # initialize the gameData every time we click on this button
            self.metaData.gameData = self.metaData.emptyGameData(self.metaData, \
            self.metaData.screen, self.metaData.song)
        elif self.targetScreen in self.metaData.mainMenu.screens:
            self.metaData.mainMenu.displaySongLoadNotice = False # re-initialze the song notice screen
            
            self.metaData.mainMenu.currScreen = self.targetScreen 
        elif self.targetScreen == 'quit':
            sys.exit()

class EndLevelButton(MainMenuButton):
    def __init__(self, posx, posy, width, height, text, backGroundColor, targetScreen, \
    metaData, onClickEvent=None, border=0, txtColor=None):
        super().__init__(posx, posy, width, height, text, backGroundColor, targetScreen, \
        metaData, onClickEvent=onClickEvent, border=border, txtColor=txtColor)

    def onClick(self): # when the button gets clicked, execute the code

        if self.targetScreen == 'menu':
            # initialize the game every time we click on this button
            self.metaData.__init__()

# when the player clicks a startLevelButton, the game will load in the data for the new song
class StartLevelButton(MainMenuButton):
    def __init__(self, posx, posy, width, height, text, backGroundColor, targetScreen, \
    metaData, onClickEvent=None, border=0, txtColor=None, checkIfSongLoaded=True):
        super().__init__(posx, posy, width, height, text, backGroundColor, targetScreen, \
        metaData, onClickEvent=onClickEvent, border=border, txtColor=txtColor)
        self.checkIfSongLoaded = checkIfSongLoaded

    def onClick(self): # when the button gets clicked, execute the code
        print('Start Game')
        print(self.metaData.song)
        if self.targetScreen == 'game':
            songName = SongSelectButton.getSongNameFromFilePath(self.metaData.song)
            # the start button only works if we have a song selected
            print(self.metaData.song)
            print('songData/' + songName + '.wav.txt')
            if os.path.isfile(self.metaData.song):
                if self.checkIfSongLoaded: # only check if the song is loaded if we want to
                    if not os.path.isfile('songData/' + songName + '.wav.txt'):
                        print('songData/' + songName + '.wav.txt')
                        self.metaData.mainMenu.displaySongLoadNotice = True
                    else:
                        self.metaData.gameData = self.metaData.emptyGameData(self.metaData, \
                        self.metaData.screen, self.metaData.song)
                        # initialize the gameData every time we click on this button
                        self.metaData.currScreen = 'game'
                else:
                    self.metaData.gameData = self.metaData.emptyGameData(self.metaData, \
                    self.metaData.screen, self.metaData.song)
                    # initialize the gameData every time we click on this button
                    self.metaData.currScreen = 'game'

# the song select buttons that are in the main menu
class SongSelectButton(MainMenuButton):
    @staticmethod
    def getSongNameFromFilePath(path):
        directories = path.split('/')
        songNameWithExtenstion = directories[-1]
        songName = songNameWithExtenstion.replace('.wav', '')
        return songName

    def __init__(self, posx, posy, width, height, backGroundColor, metaData, songFilePath, \
    onClickEvent=None, border=0, txtColor=None):
        super().__init__(posx, posy, width, height, backGroundColor=backGroundColor, \
        metaData=metaData, border=border, txtColor=txtColor)
        self.songFilePath = songFilePath
        self.songName = SongSelectButton.getSongNameFromFilePath(self.songFilePath)
        self.text = self.songName
        self.unselectedImg = 'imageAssets/unselectedButton.png'
        self.selectedImg = 'imageAssets/selectedButton.png'
        self.highlightedImg = 'imageAssets/highlightedButton.png'

    def drawButton(self, screen):
        image = pygame.image.load(self.unselectedImg)
        if self.metaData.song == 'Music/' + self.songFilePath:
            image = pygame.image.load(self.selectedImg)
        rect = image.get_rect()
        rect.centerx = self.posx + 20
        rect.centery = self.posy
        screen.blit(image, rect)

    def drawText(self, screen):
        pygame.font.init()
        txtData = pygame.font.SysFont(None,
                                self.height) # font size
        # i learned the logic for displaying texts in pygame from this wordpress
        # website
        # https://sivasantosh.wordpress.com/2012/07/18/displaying-text-in-pygame/

        text = txtData.render(self.text, True, self.txtColor, self.backGroundColor)
        rect = text.get_rect()
        textOffset = 10*len(self.text)
        rect.centerx = self.posx + 300 + textOffset
        rect.centery = self.posy
        screen.blit(text, rect)

    def draw(self, screen):
        pygame.draw.rect(screen, self.backGroundColor, self.button, self.border)
        self.drawButton(screen)
        self.drawText(screen)

    def isClicked(self, mousePosition):
        # mouse position is an (x, y) tuple
        x, y = mousePosition
        if self.posx - self.width//2 < x and self.posx + self.width//2 > x and \
        self.posy - self.height//2 < y and self.posy + self.height//2 > y:
            self.onClick()
    
    # change the target song 
    def onClick(self):
        print(self.songFilePath)
        self.metaData.song = 'Music/' + self.songFilePath

class SongPageScrollButton(Button):
    def __init__(self, posx, posy, width, height, metaData, direction=1, text=None, backGroundColor=(...), onClickEvent=None, border=0, txtColor=None):
        super().__init__(posx, posy, width, height, text=text, backGroundColor=backGroundColor, onClickEvent=onClickEvent, border=border, txtColor=txtColor)
        self.direction = direction
        self.metaData = metaData
        self.image = 'imageAssets/arrow.png'

    def isClicked(self, mousePosition):
        # mouse position is an (x, y) tuple
        x, y = mousePosition
        if self.posx - self.width//2 < x and self.posx + self.width//2 > x and \
        self.posy - self.height//2 < y and self.posy + self.height//2 > y:
            self.onClick()

    def draw(self, screen):
        pygame.font.init()
        txtData = pygame.font.SysFont(None,
                                self.height) # font size
        # i learned the logic for displaying texts in pygame from this wordpress
        # website
        # https://sivasantosh.wordpress.com/2012/07/18/displaying-text-in-pygame/
        if self.direction == 1:
            msg = '+'
        elif self.direction == -1:
            msg = '-'
        text = txtData.render(msg, True, self.txtColor, self.backGroundColor)
        rect = text.get_rect()
        rect.centerx = self.posx
        rect.centery = self.posy
        screen.blit(text, rect)
    
    def onClick(self): # when the button gets clicked, execute the code
        print('clicked!')
        if self.metaData.mainMenu.songSelectButtons.currentScreen + self.direction > -1 and \
        self.metaData.mainMenu.songSelectButtons.currentScreen + self.direction < self.metaData.mainMenu.songSelectButtons.numberOfScreens:
            self.metaData.mainMenu.songSelectButtons.currentScreen += self.direction
        print(self.metaData.mainMenu.songSelectButtons.currentScreen)
        print(self.metaData.mainMenu.songSelectButtons.numberOfScreens)
        print(self.metaData.mainMenu.songSelectButtons.buttonsPerScreen)