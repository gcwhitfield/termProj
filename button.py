# George Whitfield 
# 15-112 Term Project

import pygame

class Button:
    def __init__(self, posx, posy, width, height, color = None, border = 0):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height

        self.defaultColor = (109, 232, 102)
        self.button = pygame.Rect(self.posx, self.posy, self.width, self.height)
        if color == None:
            self.color = self.defaultColor 
        else:
            self.color = color # rgb values
    
        self.border = border

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.button, self.border)

