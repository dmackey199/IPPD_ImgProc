from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import sys
import cv2 as cv
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

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.IN)         #Read output from PIR motion sensor
camera = PiCamera()
i = 0

while i == 0:
    i = GPIO.input(8)
#     if i == 1:               #When output from motion sensor is HIGH
#         camera.start_preview()
#         sleep(5)
#         camera.capture('image.jpg')
#         camera.stop_preview()

rawCap = PiRGBArray(camera)

# Loads an image
# src = cv.imread('image.jpg', cv.IMREAD_COLOR)

for frame in camera.capture_continuous(rawCap, format="bgr", use_video_port=True):
    src = frame.array

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

    ## [draw]
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv.circle(src, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv.circle(src, center, radius, (255, 0, 255), 3)
            
    resize = ResizeWithAspectRatio(src, height=540)
    cv.imshow("Frame", resize)
    key = cv.waitKey(1) & 0xFF
    rawCap.truncate(0)
    
    if key == ord("q"):
        break

