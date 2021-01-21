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
ap.add_argument("-w", "--width", type=float, required=True,
    help="width of the left-most object in the image (in inches)")
args = vars(ap.parse_args())
# 
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
src = cv.imread('in2.jpg', cv.IMREAD_COLOR)
# v = np.median(src)
# lower = int(max(0, (1.0 - 0.33) * v))
# upper = int(min(255, (1.0 + 0.33) * v))
# can = cv.Canny(src, lower, upper)
# can = cv.Smooth(can, cv.CV_GAUSSIAN, 7, 7)
# a = 0

# for frame in camera.capture_continuous(rawCap, format="bgr", use_video_port=True):
#     src = frame.array



## [convert_to_gray]
# Convert it to gray
## [convert_to_gray]
# Convert it to gray
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
## [convert_to_gray]

# edges = cv.Canny(gray, 50, 100, 3)
# lines = cv.HoughLines(edges,1,np.pi/180,50)
# for rho,theta in lines[0]:
#     a = np.cos(theta)
#     b = np.sin(theta)
#     x0 = a*rho
#     y0 = b*rho
#     x1 = int(x0 + 1000*(-b))
#     y1 = int(y0 + 1000*(a))
#     x2 = int(x0 - 1000*(-b))
#     y2 = int(y0 - 1000*(a))
# 
#     cv.line(src,(x1,y1),(x2,y2),(0,0,255),2)

## [reduce_noise]
# Reduce the noise to avoid false circle detection
gray = cv.medianBlur(gray, 5)
## [reduce_noise]

# v = np.median(gray)
# lower = int(max(0, (1.0 - 0.75) * v))
# upper = int(min(255, (1.0 + 0.75) * v))
# can = cv.Canny(gray, lower, upper)

## [houghcircles]
rows = gray.shape[0]
circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 8,
                           param1=120, param2=30,
                           minRadius=1, maxRadius=0)
pixelsPerMetric = None
# 
# ## [draw]
if circles is not None:
    circles = np.uint16(np.around(circles))
    if len(circles[0, :]) == 2:
        for i in circles[0, :]:
            if pixelsPerMetric is None:
                pixelsPerMetric = i[2] / args["width"]
                
            center = (i[0], i[1])
            # circle outline
            size = i[2] / pixelsPerMetric
            # print(reached)
            cv.circle(src, center, i[2], (255, 0, 255), 3)
            cv.putText(src, "{:.2f}mm".format(size),
                center, cv.FONT_HERSHEY_TRIPLEX,
                2, (0, 255, 255), 2)
# 
resize = ResizeWithAspectRatio(src, height=540)
filename = 'output.jpg'
cv.imshow(filename, resize)
cv.imwrite(filename, resize)
        
# resize = ResizeWithAspectRatio(src, height=540)
# cv.imshow("Frame", resize)
# key = cv.waitKey(1) & 0xFF
# rawCap.truncate(0)
# 
# if key == ord("q"):
#     break
# 
# if a == 5:
#     quit()    

