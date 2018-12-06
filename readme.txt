George Whitfield
Andrew Id: gwhitfie
December 6, 2018
15-112 Term Project

BEATDOWN

YOUTUBE LINK
https://www.youtube.com/watch?v=6Y65BlN4CPU&list=UU8y8T-s6MUjp-I4ejrhISWA

Overview
BeatDown is a videogame that can analyze a music file and generate a level that the player needs to complete while listening to the music. The player is a green square that moves around with the computer’s mouse movement, and the enemies are colorful objects that fly across the screen with the music.


HOW TO INSTALL THE PROJECT

Clone this repository using github: git@github.com:gcwhitfield/termProj.git

Note* Make sure you are running the most recent commit on the ‘DEVELOP’ branch.

You need two outside libraries to run BeatDown:
PyAudio
Pygame

Both of these libraries can be installed using pip. If you run ‘pip install pyaudio’ and ‘pip install pygame’, it should work.

COMMON ERROR

Sometimes, you’ll try to install pyaudio and you get this error (on mac)

  src/_portaudiomodule.c:29:10: fatal error: 'portaudio.h' file not found
    #include "portaudio.h"
             ^~~~~~~~~~~~~
    1 error generated.
    error: command 'gcc' failed with exit status 1
If that happens, you need to install homebrew from https://brew.sh/  and then run 'brew install portaudio'.


SHORTCUTS

There are no shortcuts available in this project! Skipping to different sections of the song not possible with the code I currently have.


NOTES

You can’t pause the game. If you are playing a level and want to stop in the middle of it, you need to exit the window and relaunch the game.

Also, there is a small bug where BeatDown won’t close after you have played through one song. If that happens, you’re going to have to press control + C on the terminal to keyboard interrupt the BeatDown process.
