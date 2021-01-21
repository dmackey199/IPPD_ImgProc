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
vid = cv.VideoCapture('4mm_hole_test2.MP4')
# fourcc = cv.VideoWriter_fourcc(*'MPEG')
# out = cv.VideoWriter('output.avi',fourcc, 20.0, (640,480))
while (vid.isOpened()):
    ret, frame = vid.read()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    rows = gray.shape[0]
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 8,
                               param1=200, param2=30,
                               minRadius=1, maxRadius=30)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        if len(circles[0, :]) == 1:
            a = a + 1
            for i in circles[0, :]:   
                center = (i[0], i[1])
                cv.circle(frame, center, i[2], (255, 0, 255), 3)
                resize = ResizeWithAspectRatio(frame, height=540)
                filename = 'test2-out' + str(a) + '.jpg'
                cv.imwrite(filename, resize)
#     out.write(frame)
    if a == 20:
        quit()  
              

