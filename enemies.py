# George Whitfield
# 15-112 Term Project 2018

import random
import pygame
import colors

class Enemy:
    def __init__(self, metaData, size = None, speed = None):
        if size == None:
            self.size = random.randint(10, 30) # random size if none
        else:
            self.size = size

        if speed == None:
            self.speed = random.randint(1, 2) # random speed if none
        else:
            self.speed = speed
        self.metaData = metaData
        self.posx = random.randint(10, metaData.width)
        self.posy = random.randint(10, metaData.height)


class BoxEnemy(Enemy):
    def __init__(self, metaData, size=None, speed=None):
        super().__init__(metaData, size=size, speed=speed)
        self.rect = pygame.Rect(self.posx, self.posy, self.size, self.size)
        self.color = colors.Colors().RED

    def draw(self):
        pygame.draw.rect(self.metaData.screen, self.color, self.rect, 0)

    def move(self): # move normally
        self.posx += self.speed * 0.5
        self.rect = pygame.Rect(self.posx, self.posy, self.size, self.size)
    
    def beatMove(self): # move extra on the beat
        self.posx += self.speed
        self.rect = pygame.Rect(self.posx, self.posy, self.size, self.size)

    def isCollidingWithWall(self):
        if self.posx < 0 or self.posx + self.size > self.metaData.width:
            self.speed = -self.speed

class NoodleEnemy(Enemy):
    def __init__(self, metaData, size=None, speed=None):
        super().__init__(metaData, size=size, speed=speed)
