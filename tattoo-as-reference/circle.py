from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
from datetime import datetime
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
ap.add_argument("-i", "--id", type=str, required=True,
    help="the id of the mouse being observed")
ap.add_argument("-r", "--results", type=int, required=True,
    help="the number of usable measurments required")
args = vars(ap.parse_args())

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
a = 0
now = datetime.today().strftime("%b-%d-%Y")
txt = now + " results.txt"
file = open(txt, "a")
file.write("\n")
file.write("Date: " + now + "\n")
file.write("Image\tID\t\tTime\t\tMeasurement\n")
measurements = list()
times = list()

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
                               minRadius=0, maxRadius=30)
    ## [houghcircles]
    
    pixelsPerMetric = None

    ## [draw]
    unknown = False 
    if circles is not None:
        circles = np.uint16(np.around(circles))
        if len(circles[0, :]) == 2:
            if circles[0][0][1] > circles[0][1][1]:
                temp = np.copy(circles[0][0])
                circles[0][0] = circles[0][1]
                circles[0][1] = temp
            for i in circles[0, :]:
                if pixelsPerMetric is None:
                    pixelsPerMetric = i[2] / args["width"]
                    
                center = (i[0], i[1])
                # circle outline
                size = i[2] / pixelsPerMetric
                if (unknown):
                    measurements.append(size)
                    times.append(datetime.now().strftime("%H:%M:%S"))
                else:
                    unknown = True

                cv.circle(src, center, i[2], (255, 0, 255), 3)
                cv.putText(src, "{:.2f}mm".format(size),
                    center, cv.FONT_HERSHEY_TRIPLEX,
                    2, (10, 202, 55), 2)
            resize = ResizeWithAspectRatio(src, height=540)
            filename = 'Image' + str(a) + '-Mouse' + args["id"] + '.jpg'
            a = a + 1
            cv.imwrite(filename, resize)
            
    resize = ResizeWithAspectRatio(src, height=540)
    cv.imshow("Frame", resize)
    key = cv.waitKey(1) & 0xFF
    rawCap.truncate(0)
    
    if a == args["results"]:
        lowest = measurements[0]
        highest = measurements[0]
        sumup = 0
        for i in range(0, len(measurements), 1):
            file.write(str(i) + "\t\t" + args["id"] + "\t\t" + times[i] + "\t" + str(measurements[i]) + "\n")
            if measurements[i] > highest:
                highest = measurements[i]
            if measurements[i] < lowest:
                lowest = measurements[i]
            sumup = sumup + measurements[i]
        avg = sumup / a
        file.write("lowest: " + str(lowest) + "\t\thighest: " + str(highest) + "\t\taverage: " + str(avg) + "\n")
        file.close()
        quit()    

