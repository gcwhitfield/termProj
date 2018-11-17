# George Whitfield
# 15-112 Term Project 2018

import random
import pygame

class Enemy:
    def __init__(self, metaData, size = None, speed = None):
        if size == None:
            self.size = random.randint(10, 30) # random size if none
        else:
            self.size = size

        if speed == None:
            self.speed = random.randint(0, 20) # random speed if none
        else:
            self.speed = speed
        self.metaData = metaData
        self.posx = random.randint(metaData.width)
        self.posy = random.randint(metaData.height)

    def drawEnemy(self, screen):
        pass
