import subprocess
import time
import signal
import sys


# Set the to the current date and time to avoid as much overlap as possible
targetDir = time.strftime("%Y%m%d_%I%M%S")

# create the folder for all the files to be saved in for this recording
subprocess.call(['mkdir', '-p', targetDir], shell=False)

# Begin Recording all the different inputs
gameAudio = subprocess.Popen("parec --device secondrecord.monitor | lame -r - "+targetDir+"/GameAudio.mp3", shell=True)
tspeakAudio = subprocess.Popen("parec --device firstrecord.monitor | lame -r - "+targetDir+"/ChatAudio.mp3", shell=True)
microphoneAudio = subprocess.Popen("parec --device alsa_input.usb-Blue_Microphones_Yeti_Stereo_Microphone_REV8-00-Microphone.iec958-stereo | lame -r - "+targetDir+"/MicrophoneAudio.mp3", shell=True)
gameVideo = subprocess.Popen("avconv -framerate 30 -video_size 1920x1080 -f x11grab -i :0.0 -vcodec libx264 -crf 0 -preset ultrafast "+targetDir+"/Game.avi", shell=True)


# handle the interrupt that the user sends to stop recording
def signal_handler(interrupt, frame):
    print ("You pressed a button: ", interrupt)
    gameAudio.send_signal(signal.SIGTERM)
    tspeakAudio.send_signal(signal.SIGTERM)
    microphoneAudio.send_signal(signal.SIGTERM)
    gameVideo.send_signal(signal.SIGTERM)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

## Tell the user how to stop recording
print "Recording, press Ctrl+C to stop"

# wait for the user to send the interrupt
signal.pause()
