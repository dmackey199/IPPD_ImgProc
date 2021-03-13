import numpy as np
import cv2

staticCrop = [(151, 62), (581, 173)] 
greedyCrop = [(177, 60), (281, 147)]

def nothing(x):
  pass

roi = cv2.imread("img1.png",0)
clone = roi.copy()
roi = clone[staticCrop[0][1]:staticCrop[1][1], staticCrop[0][0]:staticCrop[1][0]]
#roi = clone[greedyCrop[0][1]:greedyCrop[1][1], greedyCrop[0][0]:greedyCrop[1][0]]
cv2.imshow("ROI", roi)
cv2.namedWindow('image')
cv2.createTrackbar('min','image',0,255,nothing)
cv2.createTrackbar('max','image',0,255,nothing)
cv2.namedWindow("output")

while(1):
  a = cv2.getTrackbarPos('min','image')
  b = cv2.getTrackbarPos('max','image')
  ret,thresh=cv2.threshold(roi,a,b,cv2.THRESH_BINARY_INV)
  clone = thresh;
  cv2.imshow("output",thresh)
  k = cv2.waitKey(10) & 0xFF
  if k == ord("c"):
		break

cv2.waitKey(0)
cv2.destroyAllWindows()