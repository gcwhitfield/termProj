# copied from stack overflow 
#https://stackoverflow.com/questions/6951046/pyaudio-help-play-a-file

import pyaudio
import wave
import sys
import pygame

pygame.init()
# length of data to read.
chunk = 735

# validation. If a wave file hasn't been specified, exit.

# open the file for reading.
wf = wave.open('gcslevel1.wav', 'rb')

# create an audio object
p = pyaudio.PyAudio()

# open stream based on the wave object which has been input.
stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

# read data (based on the chunk size)
data = wf.readframes(chunk)

count = 0

screen = pygame.display.set_mode(
            [
                500, # x size of the screen
                500  # y size of the screen
            ]
        )
# play stream (looping from beginning of file to the end)
while data != '':
    count += 1
    print(count)
    # writing to the stream is what *actually* plays the sound.
    stream.write(data)
    data = wf.readframes(chunk)
    pygame.display.flip
# cleanup stuff.
stream.close()    
p.terminate()