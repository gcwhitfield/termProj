# George Whitfiled
# 112 Term Project 2018
# Contain data for the decorations in the game (like the sparkl background)


import random
import math
import pygame
import colors

# basic decoration class
class Decoration:
    def __init__(self, metaData):
        self.metaData = metaData
        self.posx = random.randint(0, self.metaData.width)
        self.posy = random.randint(0, self.metaData.height)
        self.rotation = random.randint(0, 360) # angle in degrees
        self.speedx = math.cos(math.degrees(self.rotation))
        self.speedy = math.sin(math.degrees(self.rotation))
        self.moveLeftSpeed = 0.5

    def move(self):
        self.posx -= self.speedx * 0.1
        self.posy -= self.speedy * 0.1
        self.posx -= self.moveLeftSpeed * 0.2
    
    def beatMove(self):
        self.posx -= self.speedx * 1.2
        self.posy -= self.speedy * 1.2
        self.posx -= self.moveLeftSpeed 
# sparkles in the background
class Sparkle(Decoration):
    def __init__(self, metaData):
        super().__init__(metaData)
        self.color = colors.Colors().WHITE
        self.size = 1

    def leaveScreenBehavior(self): # whenever a sparkle leaves the screen, another gets added
        if self.posx < 0 - self.size or \
        self.posx > self.metaData.width + self.size or \
        self.posy < 0 - self.size or \
        self.posy > self.metaData.height + self.size:
            self.metaData.gameData.decorationsToAdd.add(Sparkle(self.metaData)) # make a new sparkle
            self.metaData.gameData.decorationsToRemove.add(self) # remove the old sparkle

    def draw(self):
        pygame.draw.circle(self.metaData.screen,
        self.color,
        (int(self.posx), int(self.posy)),
        self.size
        )