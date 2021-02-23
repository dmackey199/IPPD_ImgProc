import picamera
import argparse
from time import sleep
from datetime import datetime

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--fr", type=int, required=True,
    help="set camera framerate, up to 120 fps")
ap.add_argument("-l", "--lens", type=int, required=True,
    help="mm of lens")
ap.add_argument("-s", "--secs", type=int, required=True,
    help="time to record in seconds")
args = vars(ap.parse_args())

now = datetime.now().strftime("H%H-M%M-S%S")
name = now + "-" + str(args["lens"]) + "mm-" + str(args["fr"]) + "fps" + ".h264"

camera = picamera.PiCamera()
camera.framerate = args["fr"]

camera.start_preview()
camera.start_recording(name, format='h264')
sleep(args["secs"])
camera.stop_recording()
camera.stop_preview()

camera.close()