# copied (mostly) from stack overflow 
#https://stackoverflow.com/questions/6951046/pyaudio-help-play-a-file
# this file plays the music

import pyaudio
import wave
import sys
import time

def run(info):
    print('run')
    # length of info to read.
    chunk = 735

    # validation. If a wave file hasn't been specified, exit.

    # open the file for reading.
    wf = wave.open(info.song, 'rb')

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

    # play stream (looping from beginning of file to the end)
    while data != '': 
        data = wf.readframes(chunk)
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        info.timerFired(data)
    # cleanup stuff.
    stream.close()    
    p.terminate()