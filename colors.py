# George Whitfild
# 15-112 Term Project 2018
import math 

# I copied this clamp function from online.
# https://stackoverflow.com/questions/4092528/how-to-clamp-an-integer-to-some-range
def clamp(n, smallest, largest): return max(smallest, min(n, largest))

class Colors:
    
    # takes two colors and add them together
    @staticmethod
    def addTwoColors(c1, c2):
        result = []
        minRGB = 0
        maxRGB = 255
        for i in range(len(c1)):
            result.append(clamp(c1[i] - c2[i], minRGB, maxRGB)) # add new color value
        return result

    
    def __init__(self):
        # rgb values
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.YELLOW = (255, 255, 0)
        self.ORANGE = (255, 100, 0)
        self.TEAL = (0, 255, 200)
        self.PINK = (255, 0, 200)
    
    # go through each intensity interval and generate a color
    def calculateColorsForIntensityIntervals(self, intensity):
        veryHighColor = self.RED
        lowHighColor = self.PINK
        mediumHighColor = self.ORANGE
        mediumLowColor = self.YELLOW
        lowHighColor = self.GREEN
        veryLowColor = self.BLUE
        result = []
        # decide which color to add
        for intenVal in intensity:
            print(intenVal)
            if 0.9 < intenVal:
                result.append(veryHighColor)
            elif 0.8 < intenVal < 0.9:
                result.append(lowHighColor)
            elif 0.75 < intenVal < 0.8:
                result.append(mediumHighColor)
            elif 0.5 < intenVal < 0.75:
                result.append(mediumLowColor)
            elif 0.3 < intenVal < 0.5:
                result.append(lowHighColor)
            elif 0 < intenVal < 0.3:
                result.append(veryLowColor)
            else:
                result.append(mediumHighColor)
        # return the list of colors
        return result

    # calculate the current color of the game
    def calculateCurrentColor(self, gameData):
        result = []
        numAnimationFramesPerIntenInterval = gameData.intensityInterval // gameData.chunkSize
        colorLerp = gameData.colorLerp # how far we are along in lerping between the colors
        currColor = gameData.currMainColor
        # if there is a next color to lerp to, then do it. Otherwise, return the current interval's main color
        # the end of the song will have just one color for the last 5 seconds
        if gameData.currIntensityInterval >= (len(gameData.intensityColors) - 2):
            return currColor
        else:
            nextColor = gameData.intensityColors[gameData.currIntensityInterval + 1]
            for i in range(3): # we want co calculate the r, g, and b values so we loop three times
                distanceBetweenColors = nextColor[i] - currColor[i]
                step = distanceBetweenColors / numAnimationFramesPerIntenInterval
                print('STEP   ' + str(step))
                colorVal = (colorLerp * step) + currColor[i]
                result.append(int(colorVal)) # append the r, g, and b values to the list
            return tuple(result)
            