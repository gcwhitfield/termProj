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
        self.NoodleEnemyRate = 1
        self.NoodleTunnelRate = 0.1
# basic enemy class
class Enemy:
    def __init__(self, metaData, size = None, speed = None):
        if size == None:
            self.size = random.randint(20, 40) # random size if none
        else:
            self.size = size

        if speed == None:
            self.speed = random.randint(1, 4) # random speed if none
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
        self.spawnRate = 4
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
        return self.rect.colliderect(player.rect)

class HomingSquare(BoxEnemy):
    def __init__(self, metaData, size=None, speed=None):
        super().__init__(metaData, size=size, speed=speed)

    def moveUpDown(self):
        if self.metaData.gameData.player.posy > self.posy:
            self.posy += self.speed//4
        else:
            self.posy -= self.speed//4

    def move(self): # move normally
        self.posx -= self.speed * 0.25
        self.moveUpDown()
        self.rect = pygame.Rect(self.posx, self.posy, self.size, self.size)
        # also handle grow and shrink behavior
        super().shrink()
    
    def beatMove(self): # move extra on the beat
        self.posx -= self.speed * 1.5
        self.moveUpDown()

        super().grow()
        self.rect = pygame.Rect(self.posx, self.posy, self.size, self.size)


class NoodleEnemy(BoxEnemy):
    def __init__(self, metaData, size=None, speed=None):
        super().__init__(metaData, size=size, speed=speed)
        self.spawnRate = 4
        self.size = self.size//2 # make the noodle skinnier
        self.length = self.size * 4 # length of the noodle
        self.rect = pygame.Rect(self.posx, self.posy, self.size, self.length)
        self.colorOffset = (0, 0, 10)
        self.maxLength = self.length * 2
        self.minLength = self.length 
        self.growthRate = 2

    # draw box
    def draw(self):
        # update the color
        self.color = colors.Colors().addTwoColors(self.metaData.gameData.instantColor, self.colorOffset)
        # draw the box
        self.rect = pygame.Rect(self.posx, self.posy, self.size, self.length)
        self.rect.centerx = self.posx
        self.rect.centery = self.posy
        pygame.draw.rect(self.metaData.screen, self.color, self.rect, 0)
    
    def move(self):
        self.posx -= self.speed
        self.shrink()
    
    def grow(self):
        if self.length < self.maxLength:
            self.length += self.growthRate
        
    def shrink(self):
        if self.length > self.minLength:
            self.length -= self.growthRate * 1.2

    def beatMove(self):
        self.posx -= self.speed
        self.grow()

    def isCollidingWithPlayer(self):
        player = self.metaData.gameData.player
        return self.rect.colliderect(player.rect)

class NoodleEnemyTunnel(Enemy):
    def initializeNoodleTunnel(self, yOffset):
        result = []
        for i in range(self.numNoodles):
            # space the noodle equally
            enemPosX = self.posx + ((self.noodleWidth + self.noodleBorder) * i) 
            # calculate the y position of the noodle 
            enemPosY = (math.sin(math.radians((360 / self.noodlesPerWavePeriod) * i)) * self.waveAmplitude) \
            + yOffset + self.posy
            
            enemy = NoodleEnemy(self.metaData, size=self.noodleWidth) # make a new noodle
            enemy.posx = enemPosX
            enemy.posy = enemPosY
            enemy.speed = self.speed
            result.append(enemy)
        return result

    def __init__(self, metaData, size=None, speed=None):
        super().__init__(metaData, size=size, speed=speed)
        self.speed = random.randint(2, 4)
        self.spawnRate = .2
        self.tunnelWidth = 300 # width of the tunnel
        self.posy = random.randint(0, self.metaData.height - self.tunnelWidth)
        self.numNoodles = random.randint(100, 300)
        self.noodleWidth = 20
        self.noodleBorder = 5
        self.noodlesPerWavePeriod = random.randint(100, 200)
        self.waveAmplitude = random.randint(100, 300)
        self.totalLength = self.numNoodles * (self.noodleWidth + self.noodleBorder)

        self.upperNoodles = self.initializeNoodleTunnel(0) # y offset is 0
        self.lowerNoodles = self.initializeNoodleTunnel(self.tunnelWidth) # y offset is tunnelWidth

        self.waveAlong = 0 # number to offset wave amount by every time we move noodles
        self.waveSpeed = random.randint(5, 20)

    def noodleCrawl(self, noodls, lowerNoodles = False):
        for i in range(len(noodls)):
            noodls[i].posy = (math.sin(math.radians((360 / self.noodlesPerWavePeriod) * i) + self.waveAlong)  \
            * self.waveAmplitude) + (self.tunnelWidth * lowerNoodles) + self.posy
    
    # moves the noodles in a wave motiion
    def waveTheNoodles(self):
        self.noodleCrawl(self.upperNoodles)
        self.noodleCrawl(self.lowerNoodles, lowerNoodles = True)

    def moveNoodles(self):
        for noodl in self.upperNoodles:
            noodl.posx -= self.speed
        for noodl in self.lowerNoodles:
            noodl.posx -= self.speed

    # shrinks all of the noodles
    def shrinkNoodles(self):
        for noodl in self.upperNoodles:
            noodl.shrink()
        for noodl in self.lowerNoodles:
            noodl.shrink()
        
    # grow all of the noodles
    def growNoodles(self):
        for noodl in self.upperNoodles:
            noodl.grow()
        for noodl in self.lowerNoodles:
            noodl.grow()

    # move when off of the beat
    def move(self): # move the tunnel
        self.posx -= self.speed
        self.waveTheNoodles()
        self.moveNoodles()
        self.shrinkNoodles()

    # move when on the beat
    def beatMove(self):
        self.posx -= self.speed
        self.waveTheNoodles()
        self.moveNoodles()
        self.growNoodles()

    def draw(self):
        for noodl in self.upperNoodles:
            noodl.draw()
        for noodl in self.lowerNoodles:
            noodl.draw()

    def isCollidingWithPlayer(self):
        for noodl in self.upperNoodles:
            if noodl.isCollidingWithPlayer():
                return True
        for noodl in self.lowerNoodles:
            if noodl.isCollidingWithPlayer():
                return True
        return False

    def wallCollide(self):
        if self.posx + self.totalLength * 1.1 < 0:
            self.metaData.gameData.enemiesToRemove.add(self)

# enemy that spins in a circle and shoots bullets
class ShootySpinnyEnemy(Enemy):
    def __init__(self, metaData, size=None, speed=None):
        super().__init__(metaData, size=size, speed=speed)
        self.spawnRate = 0.25
        self.size = 30 
        self.rotationSpeed = self.speed
        self.currRotation = 0 # in degreed
        self.gunBarrelWidth = 20
        self.colorOffset = (0, 0, 50)
        self.color = colors.Colors().addTwoColors(self.colorOffset, self.metaData.gameData.instantColor)
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
        # update the color
        self.color = colors.Colors().addTwoColors(self.colorOffset, self.metaData.gameData.instantColor)
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
        self.spawnRate = 0.2
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
        # update the color
        self.color = colors.Colors().addTwoColors(self.colorOffset, self.metaData.gameData.instantColor)
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
        self.speed = 4
        self.rotation = rotation
        self.size = size
        self.colorOffset = (0, 100, 0)
        self.color = colors.Colors().addTwoColors(self.colorOffset, self.metaData.gameData.instantColor)
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
            # update the current color
            self.color = colors.Colors().addTwoColors(self.colorOffset, self.metaData.gameData.instantColor)
            pygame.draw.circle(self.metaData.screen,
            self.color,
            (int(self.posx), int(self.posy)),
            int(self.size)
            )
    
    def isCollidingWithPlayer(self):
        rect = pygame.Rect(self.posx, self.posy, int(self.size * 0.8), int(self.size * 0.8))
        return rect.colliderect(self.metaData.gameData.player.rect)
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
