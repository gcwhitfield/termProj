# George Whitfield 
# 15-112 Term Project 2018
# Player Class

import pygame
import colors

class Player:
    def __init__(self, metaData):
        self.metaData = metaData
        self.posx = self.metaData.width//2
        self.posy = self.metaData.height//2
        self.size = 30
        self.colors = colors.Colors()
        self.cursorPos = pygame.mouse.get_pos()
        self.rect = pygame.Rect(self.cursorPos, (self.size, self.size))

    # draw the player
    def draw(self):
        self.cursorPos = pygame.mouse.get_pos()
        self.posx, self.posy = self.cursorPos
        self.rect = pygame.Rect(self.cursorPos, (self.size, self.size))
        pygame.draw.rect(self.metaData.screen, self.colors.GREEN, self.rect, 0)

