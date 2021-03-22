import numpy as np
import cv2
import argparse

refPt = []
cropping = False
roi = cv2.imread("img1.png",0)
def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, cropping, roi
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		cropping = True
	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		refPt.append((x, y))
		cropping = False
		# draw a rectangle around the region of interest
		cv2.rectangle(roi, refPt[0], refPt[1], (255, 255, 255), 2)


img = cv2.imread("img1.png",0)
clone = img.copy()

def nothing(x):
  pass

cv2.namedWindow("output")
cv2.setMouseCallback("output", click_and_crop)

while(1):

  cv2.imshow("output",img)
  k = cv2.waitKey(10) & 0xFF
	# if the 'c' key is pressed, break from the loop
  if k == ord("c"):
		break


if len(refPt) == 2:
  roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
  print("Crop points: ",refPt)
  cv2.imshow("ROI", roi)
  while(1):
    k = cv2.waitKey(10) & 0xFF
    if k == ord("c"):
		break

cv2.destroyAllWindows()

cv2.namedWindow('image')
cv2.createTrackbar('min','image',0,255,nothing)
cv2.createTrackbar('max','image',0,255,nothing)

cv2.namedWindow('Threshold')
while(1):

    a = cv2.getTrackbarPos('min','image')
    b = cv2.getTrackbarPos('max','image')
    ret,thresh=cv2.threshold(roi,a,b,cv2.THRESH_BINARY_INV)
    cv2.imshow("Threshold",thresh)
    k = cv2.waitKey(10) & 0xFF
    if k == ord("c"):
		break

cv2.destroyAllWindows()