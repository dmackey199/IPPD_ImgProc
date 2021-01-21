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

a = [1,2,3,4,5,6,7,8]

while a:
    b = a.pop()
    infile = str(b) + '.png'
    src = cv.imread(infile, cv.IMREAD_COLOR)

    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    rows = gray.shape[0]
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 8,
                               param1=200, param2=30,
                               minRadius=1, maxRadius=30)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:   
            center = (i[0], i[1])
            cv.circle(src, center, i[2], (255, 0, 255), 3)

    resize = ResizeWithAspectRatio(src, height=540)
    filename = str(b) + '.jpg'
    cv.imwrite(filename, resize)
              

