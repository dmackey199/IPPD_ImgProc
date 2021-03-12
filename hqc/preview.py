import picamera
import argparse
from time import sleep

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--fr", type=int, required=True,
    help="set camera framerate, up to 90 fps")
ap.add_argument("-s", "--secs", type=int, required=True,
    help="time to record in seconds")
args = vars(ap.parse_args())

camera = picamera.PiCamera()
if args["fr"] <= 30:
    camera.resolution = (1920,1080) #30fps
elif args["fr"] <= 60:
    camera.resolution = (1280,720) #60fps
else:
    camera.resolution = (640,480) #90fps

camera.start_preview()
sleep(args["secs"])
camera.stop_preview()

camera.close()