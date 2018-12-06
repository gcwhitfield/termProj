# George Whitfield
# 15-112 Term Project 2018
# This is the most important file of the project. It takes the raw data from a 
# wav file and turns it into neatly formatted lists that the rest of the game can
# interpret easily 

import moduleManager
moduleManager.review()

import wave
import cmath
from matplotlib import pyplot as plt
import numpy
import math
import struct
import os

import string

class WavFile(object):
    # take a series of bytes and group them into 16 bit integers and return tuple of the 
    # integers. 
    def formatWavDataCorrectly(self, unformattedData):
        assert(type(unformattedData) == bytes)
        # every music sample is made up of two bytes that we need to unpack
        result = []
        unpack = struct.Struct('h').unpack
        for i in range(0, len(unformattedData), 2):
            # the h flag signifies 2 bit integer encoding
            result.append(unpack(unformattedData[i:i+2])[0]) # add each data point to the list
        return result

    # return the average loudness of the file
    def getAverageLoudness(self, data):
        numPoints = len(data)
        total = 0
        for dataPoint in data:
            dataPoint = abs(dataPoint)
            total += dataPoint
        return total // numPoints

    def getName(self, filePath):
        filePath = filePath.split('/')
        name = filePath[-1] # the name of the file
        name.replace('.wav', '')
        return name

    def __init__(self, filePath, chunkSize):
        self.frequencySpectrumData = [] # will get configured when we call the configureSpectrumData() function

        self.filePath = filePath
        self.fileName = self.getName(self.filePath)
        self.waveObject = wave.open(filePath, 'rb')
        self.sampleRate = self.waveObject.getframerate()
        self.lenInSamples = self.waveObject.getnframes()
        self.lenInSeconds = (self.lenInSamples // self.sampleRate)
        # do NOT use rawFileData because it reads every 1/2 audio frame instead of every frame.
        self.rawFileData = self.waveObject.readframes(self.lenInSamples)
        
        self.data = self.formatWavDataCorrectly(self.rawFileData)
    
        self.chunkSize = chunkSize

        #self.chunkSize = (self.lenInSamples // self.sampleRate) // 30
        # these are the frequency intervals that we will calculate the Fourier transform with
        self.frequencyBands = (
            (20, 50),
            (50, 100),
            (100, 200),
            (200, 500),
            (500, 1000),
            (1000, 2000),
            (2000, 5000),
            (5000, 10000),
            (10000, 20000)
        )
        self.calculationsPerFreqBand = 6
        self.frequencySpecsLength = len(self.frequencyBands) * self.calculationsPerFreqBand

        # AUDIO DATA VARIABLES
        self.averageLoudness = self.getAverageLoudness(self.data)
        self.loudnessPerChunk = self.getLoudnessPerChunk()
        self.maxLoudness = max(self.loudnessPerChunk)
        self.songDataFilename = self.fileName + '.txt'
        self.lowMidHighData = []

    # evaluate the fourier transform for a given frequency  ````
    def fourierEvaluate(self, wavData, frequency):
        result = 0
        # for j in range(0, self.chunkSize * 2, 2):
        for j in range(0, len(wavData) - 1, 2):
            dataPoint = wavData[j]
            i = complex(0, 1)
            k = (frequency/self.sampleRate) * 500
            exponential = cmath.exp((i*-1*cmath.pi*k*j)/((self.chunkSize)))
            result += dataPoint * exponential
        return abs(result)//50

    # return a tuple of the frequency spectrum of the data at a given time interval
    def getFrequencySpectrum(self, wavData):
        result = []
        for freqs in self.frequencyBands:
            width = freqs[1] - freqs[0]
            step = width // self.calculationsPerFreqBand
            for i in range(self.calculationsPerFreqBand):
                currFreq = freqs[0] + (i * step)
                result.append(
                    self.fourierEvaluate(wavData, currFreq)
                )
        return result

    # get a list of frequency spectrum values over time
    def freqSpectrums(self):
        result = []
        for i in range(len(self.data)//self.chunkSize):
            index1 = self.chunkSize * 2 * i
            index2 = self.chunkSize * 2 * (i + 1)
            result.append(self.getFrequencySpectrum(self.data[index1:index2]))
            print('Spectrum ' + str(i) + ' analyzed!')
        return result

    # display the audio spectrum using matplotlib and numpy
    def displayAudioSpectrum(self):
        t = numpy.array(range(self.calculationsPerFreqBand * len(self.frequencyBands)))
        plt.show()
        spectrums = self.freqSpectrums()
        for spectrum in spectrums:
            s = numpy.array(spectrum)
            plt.cla()
            plt.ylim(0, 120000)
            plt.plot(t,s)
            plt.pause(0.0000000000004)
        plt.show()
    
    # use the room mean square (RMS) to calculate the loudness of a chunk of audio
    def getLoudnessPerChunk(self):
        result = []
        for chunk in range((self.lenInSamples)//(self.chunkSize)):
            offset = int((self.chunkSize * 2) * chunk) # manipulate this value to change how the data lines up with the music
            chunkAverageLoudness = 0
            for dataPoint in range(self.chunkSize * 2):
                chunkAverageLoudness += self.data[offset + dataPoint] ** 2 # add squares
            chunkAverageLoudness = chunkAverageLoudness / self.chunkSize * 2 # divide
            chunkAverageLoudness = chunkAverageLoudness ** 0.5 # square root
            result.append(chunkAverageLoudness)
        return result

    # take the frequency data and save it as a text file
    def writeFrequencyDataToFile(self, freqData):
        result = ''
        for spectrum in freqData:
            for dataPoint in spectrum:
                result += str(int(dataPoint)) + '/'
            result += '\n'
        # the writing to file code copied from the 15-112 website
        with open('songData/' + self.songDataFilename, "wt") as f:
            f.write(result)

    # read the frequency text file
    def readFrequencyDataFile(self): # MUTABLE function
        result = []
        with open('songData/' + self.songDataFilename, 'r') as f:
            freqData = f.read()
            # append the spectrum data into the dataList
            for freqBan in freqData.splitlines():
                specData = []
                for dataPoint in freqBan.split('/'):
                    if dataPoint != '':
                        specData.append(int(dataPoint))
                result.append(specData)
        self.frequencySpectrumData = result

        
    def frameData(self, chunkSize, chunk ):
        data = self.rawFileData
        return data[chunkSize * 2 * chunk : chunkSize * 2 * (chunk + 1)]

    # This function must be called at the beginning of every level.
    def configureSpectrumData(self):
        path = 'songData/' + self.songDataFilename
        if os.path.isfile(path):
            self.readFrequencyDataFile()
        else:
            self.writeFrequencyDataToFile(self.freqSpectrums())
            self.readFrequencyDataFile()
        self.lowMidHighData = self.lowsMidsHighsSpectrum(self.frequencySpectrumData)

    # get lows, mids, and highs data for 1 interval
    def lowsMidsHighs(self, freqData):
        # lows = result[0], mids = result[1], highs = result[2]
        result = []
        for i in range(3):
            total = 0
            for dataIndex in range(len(freqData)//3):
                index = (i * (len(freqData)//3)) + dataIndex
                dataPoint = freqData[index]
                total += dataPoint
            total = total // (len(freqData) // 3)
            result.append(total)
        return result

    # get lows, mids, and highs data for the whole song
    def lowsMidsHighsSpectrum(self, freqSpectrums):
        result = []
        for spectrum in freqSpectrums:
            result.append(self.lowsMidsHighs(spectrum))
        return result
    
    # calculate the intensity for one portion of the song
    def calculateIntensity(self, lowsMidsHighsData, loudness, interval):
        intensity = 0
        loudnessAverage = 0
        for spec in range(len(lowsMidsHighsData)):
            low = lowsMidsHighsData[spec][0]
            mid = lowsMidsHighsData[spec][1]
            high = lowsMidsHighsData[spec][2]
            if low > mid > high:
                intensity += 3
            elif mid > low > high:
                intensity += 2
            else:
                intensity += 1
            
            # if we have loudness data for this interval, then use it. Else, add 1 to 
            # loudnessAverage value
            if spec > len(loudness) - 1:
                loudnessAverage += 1
            else:
                if loudness[spec] > self.averageLoudness * 1.7:
                    loudnessAverage += 3
                else:
                    loudnessAverage += 1

            
        intensity = intensity + loudnessAverage
        intensity = intensity / (self.lenInSamples//interval)
        return intensity

    #calc intensity for the whole song
    # the interval is a length in samples that we want to get data about :)
    def calcIntensityForWholeSong(self, interval, lenInSamples):
        result = []
        numChunks = self.lenInSamples // (self.chunkSize * 2)
        intervalLenInChunks = numChunks // (self.lenInSamples // interval)
        for i in range(lenInSamples//interval):
            beginning = intervalLenInChunks * i
            end = intervalLenInChunks * (i + 1)
            if end > self.lenInSamples:
                end = self.lenInSamples
                result.append(self.calculateIntensity(self.lowMidHighData[beginning:end], self.loudnessPerChunk[beginning:end], interval))
                break
            result.append(self.calculateIntensity(self.lowMidHighData[beginning:end], self.loudnessPerChunk[beginning:end], interval))
        # normalize all of the intensity values to be between 0 and 1 using the formula for standard deviation
        # learned how to take the average of a list on stack overflow 
        #https://stackoverflow.com/questions/9039961/finding-the-average-of-a-list
        instensityAverage = sum(result)/len(result)
        intensityStandardDeviation = standardDeviation(result)
        
        # normalize values according to standard deviation
        for i in range(len(result)):
            # get relative intensity
            result[i] = (result[i] - instensityAverage) / intensityStandardDeviation
        
        return result

# calculate the standard deviation of a list
def standardDeviation(lst):
    lstAv = sum(lst)/len(lst)
    weightedAv = 0
    for item in lst:
        weightedAv += (item - lstAv) ** 2
    weightedAv /= len(lst)
    stanDev = weightedAv ** 0.5
    return stanDev
