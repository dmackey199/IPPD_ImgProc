from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import sys
import cv2 as cv
import argparse
import numpy as np
import RPi.GPIO as GPIO

#from https://stackoverflow.com/questions/35180764/opencv-python-image-too-big-to-display
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv.resize(image, dim, interpolation=inter)

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--distance", type=float, required=True,
    help="distance from camera to object (in cm)")
ap.add_argument("-w", "--width", type=float, required=True,
    help="width of ear (in mm)")
args = vars(ap.parse_args())

# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(8, GPIO.IN)         #Read output from PIR motion sensor
# camera = PiCamera()
# i = 0
# 
# while i == 0:
#     i = GPIO.input(8)
#     if i == 1:               #When output from motion sensor is HIGH
#         camera.start_preview()
#         sleep(5)
#         camera.capture('image.jpg')
#         camera.stop_preview()

# rawCap = PiRGBArray(camera)

# Loads an image
src = cv.imread('4cm.jpg', cv.IMREAD_COLOR)
# a = 0

# for frame in camera.capture_continuous(rawCap, format="bgr", use_video_port=True):
# src = frame.array

## [convert_to_gray]
# Convert it to gray
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
## [convert_to_gray]

## [reduce_noise]
# Reduce the noise to avoid false circle detection
gray = cv.medianBlur(gray, 5)
## [reduce_noise]

## [houghcircles]
rows = gray.shape[0]
circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 8,
                           param1=100, param2=30,
                           minRadius=1, maxRadius=30)
## [houghcircles]

pixelsPerMetric = None

## [draw]
if circles is not None:
    circles = np.uint16(np.around(circles))
    if len(circles[0, :]) == 1:
         for i in circles[0, :]:
#             if pixelsPerMetric is None:
            focal = (i[2] * (args["distance"] * 10)) / args["width"]
                
            center = (i[0], i[1])
            # circle outline
            size = i[2] / pixelsPerMetric
            cv.circle(src, center, i[2], (255, 0, 255), 3)
            cv.putText(src, "{:.2f}mm".format(size),
                center, cv.FONT_HERSHEY_TRIPLEX,
                2, (0, 255, 255), 2)
        resize = ResizeWithAspectRatio(src, height=540)
        filename = 'image' + str(a) + '.jpg'
        a = a + 1
        cv.imwrite(filename, resize)
        
resize = ResizeWithAspectRatio(src, height=540)
cv.imshow("Frame", resize)
key = cv.waitKey(1) & 0xFF
rawCap.truncate(0)

if key == ord("q"):
    break

if a == 5:
    quit()    

