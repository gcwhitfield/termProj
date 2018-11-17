# George Whitfield
# 15-112 Term Project 2018

class GameData:
    def __init__(self, metaData):
        self.metaData = data
        self.currentBeat = 0
        self.isPaused = False
        self.pauseScreen = 0

        self.enemies = set()

    def drawGameScreen(self, screen):
        pass
    
    def drawEnemies(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)

def timerFired(metaData):
    pass