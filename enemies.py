# George Whitfield
# 15-112 Term Project 2018

import random
import pygame
import colors

class Enemy:
    def __init__(self, metaData, size = None, speed = None):
        if size == None:
            self.size = random.randint(20, 40) # random size if none
        else:
            self.size = size

        if speed == None:
            self.speed = random.randint(1, 2) # random speed if none
        else:
            self.speed = speed
        self.metaData = metaData
        self.posx = self.metaData.width
        self.posy = random.randint(self.size, metaData.height - self.size)


class BoxEnemy(Enemy):
    def __init__(self, metaData, size=None, speed=None):
        super().__init__(metaData, size=size, speed=speed)
        self.rect = pygame.Rect(self.posx, self.posy, self.size, self.size)
        self.color = colors.Colors().RED

    def draw(self):
        pygame.draw.rect(self.metaData.screen, self.color, self.rect, 0)

    def move(self): # move normally
        self.posx -= self.speed * 0.5
        self.rect = pygame.Rect(self.posx, self.posy, self.size, self.size)
    
    def beatMove(self): # move extra on the beat
        self.posx -= self.speed
        self.rect = pygame.Rect(self.posx, self.posy, self.size, self.size)

    def wallCollide(self):
        if self.posx < 0:
            self.metaData.gameData.enemiesToRemove.add(self)

class NoodleEnemy(Enemy):
    def __init__(self, metaData, size=None, speed=None):
        super().__init__(metaData, size=size, speed=speed)

# a coin isnt an enemy but it's easier to store this class in this file
class Coin:
    def __init__(self, metaData):
        self.metaData = metaData
        self.size = 10
        self.posx = random.randint(self.size, self.metaData.width - self.size)
        self.posy = random.randint(self.size, self.metaData.height - self.size)
        self.color = colors.Colors().YELLOW
        self.life = random.randint(120, 360)

    def draw(self):
        pygame.draw.circle(self.metaData.screen,
        self.color,
        (self.posx, self.posy),
        self.size
        )
    
    def lifeDrain(self):
        self.life -= 1
        if self.isDeadCoin():
            self.metaData.gameData.coinsToRemove.add(self)

    def isDeadCoin(self):
        self.metaData.gameData.maxScore += 1
        return self.life < 0
    
    def isCollidingWithPlayer(self):
        player = self.metaData.gameData.player
        return player.posx < (self.posx + self.size) < player.posx + player.size * 2 and \
               player.posy < (self.posy + self.size) < player.posy + player.size * 2
