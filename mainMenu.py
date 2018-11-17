# George Whitfield
# 15-112 Term Project 2018

import sys



class MenuData:
    def __init__(self, metaData):
        self.metaData = metaData
        self.currScreen = 'mainMenu'
        self.screens = (
            'mainMenu',
            'options',
            'fileSelect',
            'play'
        )
        self.backgroundColor = (68, 1, 96) # rgb values
        

def drawBackGround(screen, data):
    screen.fill(data.backgroundColor)

def drawMainMenu(screen, data):
    pass

def drawOptionsScreen(screen, data):
    pass

def drawFileSelect(screen, data):
    pass

def drawPlayScreen():
    pass

def draw(screen, data):
    if data.currScreen == 'mainMenu':
        drawMainMenu(screen, data)
    elif data.currScreen == 'options':
        drawOptionsScreen(screen, data)
    elif data.currScreen == 'fileSelect':
        drawFileSelect(screen, data)
    elif data.currScreen == 'play':
        drawPlayScreen(screen, data)