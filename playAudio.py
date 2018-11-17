#!usr/bin/env python  
#coding=utf-8  

# I did not create (most of)this code myself. I'm using the module PyAudio to 
# play music for the game, and I copied this code from a stack overflow
# link that contains the bare minimum needed to play audio using PyAudio.
#https://stackoverflow.com/questions/6951046/pyaudio-help-play-a-file

#import portaudio
import pyaudio  
import wave  

#define stream chunk   
chunk = 44100

#open a wav format music  
f = wave.open(r"gcslevel1.wav","rb")  
#instantiate PyAudio  
p = pyaudio.PyAudio()  
#open stream  
stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True)  
#read data  
data = f.readframes(chunk)  

#play stream  
while data:
    print('b')
    stream.write(data)  
    data = f.readframes(chunk)  

print('a')
#stop stream  
stream.stop_stream()  
stream.close()  

#close PyAudio  
p.terminate()  