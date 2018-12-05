# George Whitfield
# 15-112 Term Project 2018
# Data about the enemies in the game

import random
import pygame
import colors
import math

class EnemySpawnData:
    def init(self):
        # these are scalars that we multiply our enemy spawn rates in order to 
        # adjust how often the enemies spawn during the game
        self.BoxEnemyRate = 1
        self.ShootySpinnyEnemyRate = 0.25
        self.PlusSignShootyEnemyRate = 0.2

# basic enemy class
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
        # these centerx and centery values assume that the enemy is a square
        self.centerx = ((self.posx * 2) + self.size) // 2
        self.centery = ((self.posy * 2) + self.size) // 2

    # THIS ASSUMES THAT THE ENEMY IS A SQUARE
    def calculateCenterCoordinates(self):
        self.centerx = ((self.posx * 2) + self.size) // 2
        self.centery = ((self.posy * 2) + self.size) // 2

    # we need an empty function for isCollidingWithPlayer so we dont get an error
    def isCollidingWithPlayer(self):
        pass

# the box enemies
class BoxEnemy(Enemy):
    def __init__(self, metaData, size=None, speed=None):
        super().__init__(metaData, size=size, speed=speed)
        self.rect = pygame.Rect(self.posx, self.posy, self.size, self.size)
        self.colorOffset = (0, 10, 0)
        self.color = colors.Colors().addTwoColors(self.metaData.gameData.instantColor, self.colorOffset)
        self.minSize = self.size
        self.maxSize = self.minSize * 1.5
        self.growFactor = 1

    # draw box
    def draw(self):
        # update the color
        self.color = colors.Colors().addTwoColors(self.metaData.gameData.instantColor, self.colorOffset)
        # draw the box
        pygame.draw.rect(self.metaData.screen, self.color, self.rect, 0)
    
    # shrink the box when we aren't on the beat
    def shrink(self):
        if self.size > self.minSize:
            self.size -= self.growFactor

    # grow the box when we are on the beat
    def grow(self):
        if self.size < self.maxSize:
            self.size += self.growFactor
    
    def move(self): # move normally
        self.posx -= self.speed * 0.25
        self.rect = pygame.Rect(self.posx, self.posy, self.size, self.size)
        # also handle grow and shrink behavior
        self.shrink()
    
    def beatMove(self): # move extra on the beat
        self.posx -= self.speed * 1.5
        self.grow()
        self.rect = pygame.Rect(self.posx, self.posy, self.size, self.size)

    # if the box is colliding with the wall, then remove from game
    def wallCollide(self):
        if self.posx + self.size * 1.5 < 0:
            self.metaData.gameData.enemiesToRemove.add(self)

    # return true if the box is colliding with the player
    def isCollidingWithPlayer(self):
        player = self.metaData.gameData.player
        return player.posx < (self.posx + self.size) < player.posx + player.size * 2 and \
               player.posy < (self.posy + self.size) < player.posy + player.size * 2

class NoodleEnemy(Enemy):
    def __init__(self, metaData, size=None, speed=None):
        super().__init__(metaData, size=size, speed=speed)

# enemy that spins in a circle and shoots bullets
class ShootySpinnyEnemy(Enemy):
    def __init__(self, metaData, size=None, speed=None):
        super().__init__(metaData, size=size, speed=speed)
        self.size = 30 
        self.rotationSpeed = 1
        self.currRotation = 0 # in degreed
        self.gunBarrelWidth = 20
        self.color = (200, 100, 50)
        self.gunDistanceFromCenter = self.size // 2
        self.gunSize = self.size // 4

    # the gun position
    def getGunData(self):
        posx = self.gunDistanceFromCenter * math.cos(math.radians(self.currRotation))
        posy = self.gunDistanceFromCenter * math.sin(math.radians(self.currRotation))
        posx += self.centerx
        posy += self.centery
        posx = int(posx)
        posy = int(posy)
        gunPosition = posx, posy
        return gunPosition

    def draw(self):
        self.calculateCenterCoordinates()
        # the shooty spinny enemy is made up of two pieces - the circle, and the rectangle
        gun = self.getGunData()
        pygame.draw.circle(self.metaData.screen, self.color, gun, self.gunDistanceFromCenter//2)
        # draw the circle
        pygame.draw.circle(self.metaData.screen,
        self.color,
        (self.centerx, self.centery),
        self.size//2
        )

    def rotate(self):
        self.currRotation += 1 * self.rotationSpeed

    def move(self):
        self.posx -= self.speed
        self.rotate()

    def beatMove(self): # move extra on the beat
        self.posx -= self.speed * 1.5
        self.posx = int(self.posx)
        gunposx, gunposy = self.getGunData()
        self.metaData.gameData.bulletsToAdd.add(Bullet(
            self.metaData, 
            gunposx, # spawn bullet at the gun position
            gunposy,
            self.currRotation, 
            self.gunSize))
        self.rotate()
    
    def wallCollide(self):
        if self.posx - self.size * 1.5 < 0:
            self.metaData.gameData.enemiesToRemove.add(self)

    def isCollidingWithPlayer(self):
        player = self.metaData.gameData.player
        return player.posx < (self.posx + self.size) < player.posx + player.size * 2 and \
               player.posy < (self.posy + self.size) < player.posy + player.size * 2

        
# enemy that shoots bullets in a plus sign
class PlusSignShootyEnemy(ShootySpinnyEnemy):
    def __init__(self, metaData, size=None, speed=None):
        super().__init__(metaData, size=size, speed=speed)
        self.tgunAngle = self.currRotation
        self.rgunAngle = self.currRotation + 270
        self.lgunAngle = self.currRotation + 90
        self.bgunAngle = self.currRotation + 180

    def move(self):
        self.posx -= self.speed
        self.rotate()
        #self.rotate()

    # calculate the coordinates of the guns. This is what makes the enemy look like it spins in a circle
    def calculateLeftRightBottomGunsData(self, topGunData):
        # update the gun rotations
        self.tgunAngle = self.currRotation
        self.rgunAngle = self.currRotation + 270
        self.lgunAngle = self.currRotation + 90
        self.bgunAngle = self.currRotation + 180
        # get the gun positions
        topGunPosx, topGunPosy = self.getGunData()
        leftGunPosx = self.centerx + self.size//2 * math.cos(math.radians(self.lgunAngle))
        leftGunPosy = self.centery + self.size//2 * math.sin(math.radians(self.lgunAngle))
        rightGunPosx = self.centerx + self.size//2 * math.cos(math.radians(self.rgunAngle))
        rightGunPosy = self.centery + self.size//2 * math.sin(math.radians(self.rgunAngle))
        bottomGunPosx = self.centerx + self.size//2 * math.cos(math.radians(self.bgunAngle))
        bottomGunPosy = self.centery + self.size//2 * math.sin(math.radians(self.bgunAngle))
        return int(topGunPosx), int(topGunPosy), int(leftGunPosx), int(leftGunPosy), \
        int(rightGunPosx), int(rightGunPosy), int(bottomGunPosx), int(bottomGunPosy)
    
    def beatMove(self): # move extra on the beat
        # move the enemy
        self.posx -= self.speed * 1.5
        self.posx = int(self.posx)
        # calculate gun positions and angles
        tgunx, tguny, lgunx, lguny, rgunx, rguny, bgunx, bguny = self.calculateLeftRightBottomGunsData(self.getGunData())
        # add the corresponding bullets
        # top bullet
        self.metaData.gameData.bulletsToAdd.add(Bullet(
            self.metaData, 
            tgunx,
            tguny,
            self.tgunAngle, 
            self.gunSize))
        # left bullet
        self.metaData.gameData.bulletsToAdd.add(Bullet(
            self.metaData, 
            lgunx,
            lguny,
            self.lgunAngle, 
            self.gunSize))
        # right bullet
        self.metaData.gameData.bulletsToAdd.add(Bullet(
            self.metaData, 
            rgunx,
            rguny,
            self.rgunAngle, 
            self.gunSize))
        # bottom bullet
        self.metaData.gameData.bulletsToAdd.add(Bullet(
            self.metaData, 
            bgunx,
            bguny,
            self.bgunAngle, 
            self.gunSize))
        self.rotate()

    def draw(self):
        self.calculateCenterCoordinates()
        # the shooty spinny enemy is made up of two pieces - the circle, and the rectangle
        tgunx, tguny, lgunx, lguny, rgunx, rguny, bgunx, bguny = self.calculateLeftRightBottomGunsData(self.getGunData())
        
        # draw top gun
        pygame.draw.circle(self.metaData.screen, self.color, (tgunx, tguny), self.gunDistanceFromCenter//2)
        # draw left gun
        pygame.draw.circle(self.metaData.screen, self.color, (lgunx, lguny), self.gunDistanceFromCenter//2)
        # draw right gun
        pygame.draw.circle(self.metaData.screen, self.color, (rgunx, rguny), self.gunDistanceFromCenter//2)
        # draw bottom gun
        pygame.draw.circle(self.metaData.screen, self.color, (bgunx, bguny), self.gunDistanceFromCenter//2)
        # draw the middle circle
        pygame.draw.circle(self.metaData.screen,
        self.color,
        (self.centerx, self.centery),
        self.size//2
        )
    
class Bullet(Enemy):
    def __init__(self, metaData, posx, posy, rotation, size, speed=None, color=None):
        super().__init__(metaData)
        self.posx = posx
        self.posy = posy
        self.speed = 3
        self.rotation = rotation
        self.size = size
        self.color = (0, 200, 200)
        self.isDead = False

    # a collision for the bullet object is hitting any wall
    def wallCollide(self):
        if self.posx < 0 - self.size or \
        self.posx > self.metaData.width + self.size or \
        self.posy < 0 - self.size or \
        self.posy > self.metaData.height + self.size:
            self.metaData.gameData.enemiesToRemove.add(self)
            self.isDead = True
    
    def move(self):
        self.posx += self.speed * math.cos(math.radians(self.rotation))
        self.posy += self.speed * math.sin(math.radians(self.rotation))

    def beatMove(self): # move extra on the beat
        self.posx += self.speed * 1.5 * math.cos(math.radians(self.rotation))
        self.posy += self.speed * 1.5 * math.sin(math.radians(self.rotation))

    def draw(self):
        if not self.isDead:
            pygame.draw.circle(self.metaData.screen,
            self.color,
            (int(self.posx), int(self.posy)),
            int(self.size)
            )

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
