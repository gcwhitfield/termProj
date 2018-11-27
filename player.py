import pygame
import colors

class Player:
    def __init__(self, metaData):
        self.metaData = metaData
        self.posx = self.metaData.width//2
        self.posy = self.metaData.height//2
        self.size = 30
        self.colors = colors.Colors()

    # draw the player
    def draw(self):
        cursorPos = pygame.mouse.get_pos()
        self.posx, self.posy = cursorPos
        rect = pygame.Rect(cursorPos, (self.size, self.size))
        pygame.draw.rect(self.metaData.screen, self.colors.GREEN, rect, 0)

