#! /usr/bin/python

import subprocess
import time
import signal
import sys
import os
import re


audioChannels = ['Game', 'Chat']

# Valid sample rates are 8, 11.025, 12, 16, 22.05, 24, 32, 44.1, and 48
audioSampleKilorate = 48
audioSampleRate = audioSampleKilorate * 1000

# The pulse audio device name of the microphone to record
microphoneDeviceName = "alsa_input.usb-Blue_Microphones_Yeti_Stereo_Microphone_REV8-00-Microphone.iec958-stereo"

# Destination Folder
destinationFolder = os.path.abspath('.')

# If there are no arguments included in the command print out the possible arguments
if (len(sys.argv) < 2):
    print "Use the arguments\n  configure - configure pulse audio channels\n  record - Record the screen\n  Compress - Compress the video and audio files"
    quit()

# If we are supposed to begin recording start recording
if (sys.argv[1] == 'record'):
    # Set the to the current date and time to avoid as much overlap as possible
    targetDir = os.path.join(destinationFolder, time.strftime("%Y%m%d_%H%M%S"))

    # create the folder for all the files to be saved in for this recording
    subprocess.call(['mkdir', '-p', targetDir], shell=False)

    # Begin Recording all the different inputs
    audioRecordingProcesses = {};
    for audioChannel in audioChannels:
        softwareAudioCommand = "parec --rate %d --device %s | lame -r -s %d - %s/%sAudio.mp3" % (audioSampleRate, audioChannel+"Record.monitor", audioSampleKilorate, targetDir, audioChannel)
        audioRecordingProcesses[audioChannel] = subprocess.Popen(softwareAudioCommand, shell=True)

    microphoneAudioCommand = "parec --rate %d --device %s | lame -r -s %d - %s/%sAudio.mp3" % (audioSampleRate, microphoneDeviceName, audioSampleKilorate, targetDir, "Microphone")
    microphoneAudio = subprocess.Popen(microphoneAudioCommand, shell=True)

    gameVideo = subprocess.Popen("avconv -video_size 1920x1080 -f x11grab -i :0.0 -vcodec libx264 -qp 0 -preset ultrafast "+targetDir+"/Game.mp4", shell=True)

    # handle the interrupt that the user sends to stop recording
    def signal_handler(interrupt, frame):
        print ("You pressed a button: ", interrupt)
        for audioChannel in audioChannels:
            audioRecordingProcesses[audioChannel].send_signal(signal.SIGTERM)
        microphoneAudio.send_signal(signal.SIGTERM)
        gameVideo.send_signal(signal.SIGTERM)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    ## Tell the user how to stop recording
    print "Recording, press Ctrl+C to stop"

    # wait for the user to send the interrupt
    signal.pause()


# If we are supposed to set up the pulse audio config then print out the commands to do so
elif (sys.argv[1] == 'configure'):
    print "Beginning Configuration"
    print "Run the commands"

    for audioChannel in audioChannels:
        print 'pactl load-module module-null-sink sink_name='+audioChannel+'Record sink_properties=device.description="'+audioChannel+'RecordingOnly"'
    for audioChannel in audioChannels:
        print 'pacmd load-module module-combine-sink sink_name='+audioChannel+'Combine sink_properties=device.description="'+audioChannel+'RecordingCombine" slaves=alsa_output.pci-0000_00_14.2.analog-stereo,'+audioChannel+'Record'

elif (sys.argv[1] == 'compress'):
    if (len(sys.argv) < 3):
        print 'You must specify a folder to compress, you can also use LAST to compress the most recent folder'
        quit()

    directoryFullPath = "";
    if (sys.argv[2] == "LAST"):
        mostRecentFolder = sorted([x for x in os.walk(destinationFolder).next()[1] if re.match("\d{8}_\d{6}$" ,x)])[-1]

        m = re.match("(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})", mostRecentFolder);
        print "Most Recent Folder was recorded on " + m.group(1) + "/" + m.group(2) + "/" + m.group(3) + " at " + m.group(4) + ":" + m.group(5)

        directoryFullPath = os.path.join(destinationFolder, mostRecentFolder);
    else:
        directoryFullPath = os.path.abspath(sys.argv[2])


    # Generate the full path with flags for all of the non-microphone audio streams
    additionalAudioFiles = "".join(["-i " + os.path.join(directoryFullPath, x+"Audio.mp3") + " " for x in audioChannels])
    # Generate the full path for the input Microphone audio
    microphoneAudioFile = os.path.join(directoryFullPath, "MicrophoneAudio.mp3")
    # Generate the full path for the input video file
    inputVideoFile = os.path.join(directoryFullPath, "Game.mp4")
    # generate the full path for the output file
    outputVidoeFile = os.path.join(directoryFullPath, "Final.mp4")

    # Composit the commmand together into a single command
    compressionCommand = "avconv -i "+inputVideoFile+" -i "+microphoneAudioFile+" " + additionalAudioFiles + " -r 30 -codec:a libmp3lame " + outputVidoeFile

    finalVideo = subprocess.Popen(compressionCommand, shell=True)

    # handle the interrupt that the user sends to stop recording
    def signal_handler(interrupt, frame):
        print ("You pressed a button: ", interrupt)
        finalVideo.send_signal(signal.SIGTERM)

    signal.signal(signal.SIGINT, signal_handler)

    # Tell the user how to stop converting if nessasary
    print "Recording, press Ctrl+C to stop"

    finalVideo.wait()
