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
            result.append(unpack(unformattedData[i:i+2])[0])
        return result

    def __init__(self, filePath):
        self.filePath = filePath
        self.waveObject = wave.open(filePath, 'r')
        self.sampleRate = self.waveObject.getframerate()
        self.lenInSamples = self.waveObject.getnframes()
        self.lenInSeconds = (self.lenInSamples // self.sampleRate)
        # do NOT use rawFileData because it reads every 1/2 audio frame instead of every frame.
        self.rawFileData = self.waveObject.readframes(self.lenInSamples)

        self.data = self.formatWavDataCorrectly(self.rawFileData)
    
        self.fourierBinSize = self.sampleRate//30

        #self.fourierBinSize = (self.lenInSamples // self.sampleRate) // 30
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

    # evaluate the fourier transform for a given frequency  ````
    def fourierEvaluate(self, wavData, frequency):
        result = 0
        for j in range(0, self.fourierBinSize, 2):
            dataPoint = wavData[j]
            i = complex(0, 1)
            k = (frequency/self.sampleRate) * 100
            exponential = cmath.exp((i*-1*cmath.pi*k*j)/((self.fourierBinSize)))
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
                result.append(tuple([
                    self.fourierEvaluate(wavData, currFreq)
                ]))
        return result

    # get a list of frequency spectrum values over time
    def freqSpectrums(self, wavData):
        result = []
        for i in range(len(wavData)//self.fourierBinSize):
            index1 = self.fourierBinSize * i
            index2 = self.fourierBinSize * (i + 1)
            result.append(self.getFrequencySpectrum(wavData[index1:index2]))

        return result

    def displayAudioSpectrum(self):
        t = numpy.array(range(self.calculationsPerFreqBand * len(self.frequencyBands)))
        plt.show()
        spectrums = self.freqSpectrums(self.data)
        print('calc complete')
        for spectrum in spectrums:
            s = numpy.array(spectrum)
            #print(spectrum)
            plt.cla()
            plt.ylim(0, 120000)
            plt.plot(t,s)
            plt.pause(0.0000000000004)
        #s = numpy.array(s)


        plt.show()

testFile = WavFile('notestest2.wav')
#testFile.displayAudioSpectrum()
print(len(testFile.data))
testFile.displayAudioSpectrum()


