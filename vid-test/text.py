import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from picamera import PiCamera
from time import sleep
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import argparse
import imutils
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.IN)         #Read output from PIR motion sensor
camera = PiCamera()
camera.resolution = (2592, 1944)
camera.framerate = 15
i = GPIO.input(8)

while i == 0:
    i = GPIO.input(8)
    if i == 1:               #When output from motion sensor is HIGH
        camera.start_preview()
        sleep(5)
        camera.capture('image.jpg')
        camera.stop_preview()

img = cv.imread('image.jpg',0)
edges = cv.Canny(img,100,200)
plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()