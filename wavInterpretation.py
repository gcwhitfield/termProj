# George Whitfield
# 15-112 Term Project 2018
import moduleManager
moduleManager.review()

import wave
import cmath
from matplotlib import pyplot as plt
import numpy
import math
import struct

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


    # evaluate the fourier transform for a given frequency  ````
    def fourierEvaluate(self, wavData, frequency):
        result = 0
        for j in range(0, self.chunkSize, 2):
            dataPoint = wavData[j]
            i = complex(0, 1)
            k = (frequency/self.sampleRate) * 100
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
                #print('i = ' + str(i))
                currFreq = freqs[0] + (i * step)
                result.append(
                    self.fourierEvaluate(wavData, currFreq)
                )
        return result

    # get a list of frequency spectrum values over time
    def freqSpectrums(self):
        result = []
        for i in range(len(self.data)//self.chunkSize):
            index1 = self.chunkSize * i
            index2 = self.chunkSize * (i + 1)
            result.append(self.getFrequencySpectrum(self.data[index1:index2]))
        return result

    # display the audio spectrum using matplotlib and numpy
    def displayAudioSpectrum(self):
        t = numpy.array(range(self.calculationsPerFreqBand * len(self.frequencyBands)))
        plt.show()
        spectrums = self.freqSpectrums(self.data)
        print('calc complete')
        for spectrum in spectrums:
            s = numpy.array(spectrum)
            plt.cla()
            plt.ylim(0, 120000)
            plt.plot(t,s)
            plt.pause(0.0000000000004)
        plt.show()
    
    # calculate the average loudness per chunk of audio
    def getLoudnessPerChunk(self):
        result = []
        for chunk in range(self.lenInSamples//self.chunkSize):
            offset = self.chunkSize * chunk
            chunkAverageLoudness = 0
            for dataPoint in range(self.chunkSize):
                chunkAverageLoudness += abs(self.data[offset + dataPoint])
            chunkAverageLoudness = chunkAverageLoudness / self.chunkSize
            result.append(chunkAverageLoudness)
        return result

    # take the frequency data and save it as a text file
    def writeFrequencyDataToFile(self, freqData):
        print('write to file')
        result = ''
        #print(freqData)
        for spectrum in freqData:
            for dataPoint in spectrum:
                result += str(int(dataPoint)) + '/'
            result += '\n'
        songDataFilename = self.fileName + '.txt'
        # the writing to file code copied from the 15-112 website
        with open('songData/' + songDataFilename, "wt") as f:
            f.write(result)

    # read the frequency text file
    def readFrequencyDataFile(self, dataList): # MUTABLE function
        print('readFile')
        songDataFilename = self.fileName + '.txt'
        with open('songData/' + songDataFilename, 'r') as f:
            freqData = f.read()
            # append the spectrum data into the dataList
            for freqBan in freqData.splitlines():
                specData = []
                for dataPoint in freqBan.split('/'):
                    if dataPoint != '':
                        specData.append(int(dataPoint))
                dataList.append(specData)


testFile = WavFile('notesTest3.wav', 2205)

#print(testFile.lenInSamples)

#print(testFile.chunkSize)
#testFile.displayAudioSpectrum()
#testFile.displayAudioSpectrum()






