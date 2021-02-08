#Courtesy of https://stackoverflow.com/questions/45836214/opencv-python-count-pixels

import numpy as np
import cv2
import argparse

refPt = []
cropping = False
roi = cv2.imread("circles.png",0)
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
		cv2.imshow("debug", roi)

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
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

    return cv2.resize(image, dim, interpolation=inter)

ap = argparse.ArgumentParser()
ap.add_argument("-w", "--width", type=float, required=True,
    help="width of the left-most object in the image (in inches)")
args = vars(ap.parse_args())

img=cv2.imread("circles.png",0)

    ## [convert_to_gray]
    # Convert it to gray
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
## [convert_to_gray]

## [reduce_noise]
# Reduce the noise to avoid false circle detection
gray = cv2.medianBlur(img, 5)
# ## [reduce_noise]

# ## [houghcircles]
rows = gray.shape[0]
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                            param1=100, param2=30,
                            minRadius=0, maxRadius=30)
# ## [houghcircles]

pixelsPerMetric = None

# [draw]
# unknown = False 
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

##


#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def nothing(x):
  pass

cv2.namedWindow('image')

clone = gray.copy()

cv2.createTrackbar('min','image',0,255,nothing)
cv2.createTrackbar('max','image',0,255,nothing)
cv2.namedWindow("output")
cv2.setMouseCallback("output", click_and_crop)

while(1):

  a = cv2.getTrackbarPos('min','image')
  b = cv2.getTrackbarPos('max','image')
  ret,thresh=cv2.threshold(img,a,b,cv2.THRESH_BINARY_INV)
  clone = thresh;
  cv2.imshow("output",thresh)
  k = cv2.waitKey(10) & 0xFF
  if k == ord("r"):
		thresh = clone.copy()
	# if the 'c' key is pressed, break from the loop
  elif k == ord("c"):
		break


if len(refPt) == 2:
  roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
  cv2.imshow("ROI", roi)
  while(1):
    k = cv2.waitKey(10) & 0xFF
    calculatedArea = cv2.countNonZero(thresh) * pixelsPerMetric
    if k == 27:
      break
print "Pixel Count: ", cv2.countNonZero(roi)
print "Area is mm: ", calculatedArea
cv2.destroyAllWindows()