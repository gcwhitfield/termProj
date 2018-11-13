# George Whitfield
# 15-112 Term Project 2018

import moduleManager
moduleManager.review()

import wave
import struct
from matplotlib import pyplot as plt
import numpy as np

# import a wav file and print out the frame data at 10

wavFile = wave.open('gcslevel1.wav', 'rb')
frameTime = 10
# for i in range(0, 10):
wavFile.setpos(1)
#print(wavFile.tell())
wavFile.setpos(5)
wavFile.setpos(100)
print(wavFile.getnframes())
print(wavFile.getframerate())

#print(wavFile.tell())
#print(wavFile.readframes(3))

#print(struct.unpack('h', bytes('''\x8e'''.encode())))

i = 0
def getIndividualBytes(bytesInfo):
    #print(type(bytesInfo))
    #print('bytes = ')
    #print(bytesInfo)
    info = []
    #bytesInfo = str(bytesInfo)
    # remove the b' and the final '
    # bytesInfo = bytesInfo[2:-1]
    i = 0
    for byte in bytesInfo:
        i += 1
        #print('byte = ' + str(byte))
        #print(byte)
        info.append(int(byte))
        if i > 1000:
            break
    print(info)
    return info

#getIndividualBytes(wavFile.readframes(100000))

import matplotlib.pyplot as plt



# Data for plotting

t = np.array(range(1001))
s = np.array([179, 0, 205, 255, 179, 0, 196, 255, 183, 0, 191, 255, 183, 0, 184, 255, 186, 0, 178, 255, 184, 0, 170, 255, 183, 0, 163, 255, 178, 0, 154, 255, 175, 0, 146, 255, 169, 0, 136, 255, 163, 0, 128, 255, 157, 0, 119, 255, 150, 0, 111, 255, 142, 0, 102, 255, 132, 0, 93, 255, 123, 0, 84, 255, 112, 0, 75, 255, 101, 0, 67, 255, 88, 0, 58, 255, 77, 0, 50, 255, 63, 0, 42, 255, 51, 0, 35, 255, 37, 0, 27, 255, 25, 0, 20, 255, 9, 0, 13, 255, 253])
#print(len())
print(t)
print(len(t))

plt.plot(range(101), [179, 0, 205, 255, 179, 0, 196, 255, 183, 0, 191, 255, 183, 0, 184, 255, 186, 0, 178, 255, 184, 0, 170, 255, 183, 0, 163, 255, 178, 0, 154, 255, 175, 0, 146, 255, 169, 0, 136, 255, 163, 0, 128, 255, 157, 0, 119, 255, 150, 0, 111, 255, 142, 0, 102, 255, 132, 0, 93, 255, 123, 0, 84, 255, 112, 0, 75, 255, 101, 0, 67, 255, 88, 0, 58, 255, 77, 0, 50, 255, 63, 0, 42, 255, 51, 0, 35, 255, 37, 0, 27, 255, 25, 0, 20, 255, 9, 0, 13, 255, 253])

plt.plot(t, s)
plt.show()

# returns a one-D list of of 50 frequency amplitudes from 40 herts to 20 kiloHertz
def calCulateFrequencySpectrum(waveData):
    minFrequency = 40 # hertz
    maxFrequency
def getFourierTransform(waveData, numBins):
    for n in numBins:
        pass