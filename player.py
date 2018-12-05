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
        self.textColor = (0, 0, 0) # black
        self.size = 50
        self.colors = colors.Colors()
        self.cursorPos = pygame.mouse.get_pos()
        self.rect = pygame.Rect(self.cursorPos, (self.size, self.size))
        self.color = self.colors.GREEN

    # draw the player
    def draw(self):
        self.cursorPos = pygame.mouse.get_pos()
        self.posx, self.posy = self.cursorPos
        self.rect = pygame.Rect(self.cursorPos, (self.size, self.size))
        pygame.draw.rect(self.metaData.screen, self.color, self.rect, 0)
        self.drawScore()

    def drawScore(self):
        score = str(self.metaData.gameData.score) # current game score
        txtData = pygame.font.SysFont(None,
                                self.size//2) # font size
        # i learned the logic for displaying texts in pygame from this wordpress
        # website
        # https://sivasantosh.wordpress.com/2012/07/18/displaying-text-in-pygame/

        text = txtData.render(score, True, self.textColor, self.color)
        rect = text.get_rect()
        rect.centerx = self.posx + self.size//2 # get the center of the player
        rect.centery = self.posy + self.size//2 
        self.metaData.screen.blit(text, rect)

