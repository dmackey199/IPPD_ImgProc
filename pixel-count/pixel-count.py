#Courtesy of https://stackoverflow.com/questions/45836214/opencv-python-count-pixels

import numpy as np
import cv2

img=cv2.imread("box.png",0)

def nothing(x):
  pass

cv2.namedWindow('image')

cv2.createTrackbar('min','image',0,255,nothing)
cv2.createTrackbar('max','image',0,255,nothing)

while(1):

 a = cv2.getTrackbarPos('min','image')
 b = cv2.getTrackbarPos('max','image')
 ret,thresh=cv2.threshold(img,a,b,cv2.THRESH_BINARY_INV)
 cv2.imshow("output",thresh)
 k = cv2.waitKey(10) & 0xFF
 if k == 27:
    break
print cv2.countNonZero(thresh)
cv2.destroyAllWindows()