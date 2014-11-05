Description
--------------------------------------------------------------------------------
This is a simple program for recording audio and video on a Linux desktop
This program will record individual pulse audio sink-sources (or sources, monitors, or whatever they are called) to mp3 files
This program will also record video via avconv (fork of ffmpeg)


Goals
--------------------------------------------------------------------------------
- Have a program that can start and stop all the recordings at once
- Have a script to help setup pulseaudio channels to allow for more precise recording
- Have either a ConfigFile or a set of simple command line arguments for recoding data


Reach Goals
--------------------------------------------------------------------------------
- Some sort of UI (ncurses or QT) that interfaces with the command line


Purpose
--------------------------------------------------------------------------------
On windows I used to use a program called loilo which captured audio and video
together and save it as a nearly uncompressed file. This file was great for
editing and could be easily compressed afterwards then uploaded or transfered to
wherever. Having made another push to try to switch to fully switch to Linux I
decided that I should also be able to record video in Linux so I found
recordmydesktop which was a great program but was unable to record audio
separately and tried to encode the video immediately after it finished
recording. This program will save a nearly uncompress video source and will be
able to record audio directly out of pulseaudio monitors.

