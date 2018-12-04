# George Whitfild
# 15-112 Term Project 2018

class Colors:
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
        # return the list of colors
        return result

    def calculateCurrentColor(self, colorsList, sampleRate, lengthOfIntensityIntervalInSeconds):
        result = []
        for colorVal in range(3): # we want co calculate the r, g, and b values so we loop three times
            distanceBetweenColors = 0
        return tuple(result)
            