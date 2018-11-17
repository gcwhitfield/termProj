# George Whitfield
# 15-112 Term Project 2018

import moduleManager
moduleManager.review()

import sys
import pygame

pygame.init()
size = width, height = 320, 820
speed = [1, 3]
black = 0, 0, 0

screen = pygame.display.set_mode(size)


size = (30, 30)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
   
    cursorpos = pygame.mouse.get_pos() 
    print(cursorpos)
    boxrect = pygame.Rect(cursorpos, size)
    '''
    boxrect = boxrect.move(speed)
    if boxrect.left < 0 or boxrect.right > width:
        speed[0] = -speed[0]
        if speed[0] > 0:
            speed[0] += 1
        else:
            speed[0] -= 1
    if boxrect.top < 0 or boxrect.bottom > height:
        speed[1] = -speed[1]
        if speed[1] > 0:
            speed[1] += 1
        else:
            speed[1] -= 1
    '''
    
    screen.fill(black)
    pygame.draw.rect(screen, (100, 100, 100), boxrect, 0)
    pygame.display.flip()