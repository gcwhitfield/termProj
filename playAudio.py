#!usr/bin/env python  
#coding=utf-8  

# I did not create (most of) this code myself. I'm using the module PyAudio to 
# play music for the game, and I copied this code from a stack overflow
# link that contains the bare minimum needed to play audio using PyAudio.
#https://stackoverflow.com/questions/6951046/pyaudio-help-play-a-file

#import portaudio
import pyaudio  
import wave 
from wavInterpretation import WavFile

#instantiate PyAudio  
p = pyaudio.PyAudio()  

print('1')
#open a wav format music  
song = gameData.songObject

songWaveFile = wave.open(gameData.song)
print('2')
class FrameData:
    def __init__(self, currLoudness, frequencies):
        self.currLoudness = currLoudness
        self.frequencies = frequencies
        self.averageLoudness = song.averageLoudness
#open stream  
stream = p.open(format = p.get_format_from_width(song.waveObject.getsampwidth()),  
                channels = song.waveObject.getnchannels(),  
                rate = song.waveObject.getframerate(),  
                output = True)  
#define stream chunk   
print('3')


#read data  
data = songWaveFile.readframes(chunk)

def stream(chunksize, gameData):
    chunk = gameData.chunk
    gameData.gameTime += 1
    print('b')
        
    # data = songWaveFile.readframes(chunk) 
    frameData = FrameData(
        song.loudnessPerChunk[gameData.gameTime],
        (0, 0, 0)
    )
    stream.write(data) 
    gameData.timerFired(frameData)

'''
#play stream  
while data:
    gameData.gameTime += 1
    print('b')
    stream.write(data)  
    data = songWaveFile.readframes(chunk) 
    frameData = FrameData(
        song.loudnessPerChunk[gameData.gameTime],
        (0, 0, 0)
    ) 
    gameData.timerFired(frameData)
'''

print('a')
#stop stream  
stream.stop_stream()  
stream.close()  

#close PyAudio  
p.terminate()  