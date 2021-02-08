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

a = 0
camera = PiCamera()
camera.resolution = (1920, 1080)
camera.framerate = 15
rawCap = PiRGBArray(camera)

for frame in camera.capture_continuous(rawCap, format="bgr", use_video_port=True):
    src = frame.array

    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    gray = cv.medianBlur(gray, 5)
    rows = gray.shape[0]
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 8,
                               param1=100, param2=30,
                               minRadius=0, maxRadius=30)
    
    resize = ResizeWithAspectRatio(src, height=540)
                
    if circles is not None:
        circles = np.uint16(np.around(circles))
        if len(circles[0, :]) == 2:
            a = a + 1
            for i in circles[0, :]:   
                center = (i[0], i[1])
                cv.circle(src, center, i[2], (255, 0, 255), 3)
                resize = ResizeWithAspectRatio(src, height=540)
                filename = 'img' + str(a) + '.jpg'
                cv.imwrite(filename, resize)
    
    cv.imshow("Frame", resize)
    key = cv.waitKey(1) & 0xFF
    rawCap.truncate(0)
    
#     out.write(frame)
    if a == 5:
        quit()  
              

