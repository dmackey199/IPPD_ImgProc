import numpy as np
import cv2

staticCrop = [(151, 62), (581, 173)] 
greedyCrop = [(177, 60), (281, 147)]

def nothing(x):
  pass

image = cv2.imread("img1.png")

new_image = np.zeros(image.shape, image.dtype)
alpha = 1.5;
beta = 20;
new_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

cv2.imshow('Original Image', image)
cv2.imshow('New Image', new_image)
# Wait until user press some key
cv2.waitKey()

# roi = cv2.imread("img1.png")
# gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
# clone = gray.copy()
# #roi = clone[staticCrop[0][1]:staticCrop[1][1], staticCrop[0][0]:staticCrop[1][0]]
# roi = clone[greedyCrop[0][1]:greedyCrop[1][1], greedyCrop[0][0]:greedyCrop[1][0]]

# cv2.imshow("ROI", roi)
# cv2.waitKey(0)

#HoughCircles
# output = roi.copy()
# circles = cv2.HoughCircles(roi, cv2.HOUGH_GRADIENT, 1, 10)
# if circles is not None:
# 	# convert the (x, y) coordinates and radius of the circles to integers
# 	circles = np.round(circles[0, :]).astype("int")
# 	# loop over the (x, y) coordinates and radius of the circles
# 	for (x, y, r) in circles:
# 		# draw the circle in the output image, then draw a rectangle
# 		# corresponding to the center of the circle
# 		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
# 		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
# 	# show the output image
# 	cv2.imshow("output", np.hstack([roi, output]))
# 	cv2.waitKey(0)
# else:
#   print("No Circles found")

#thresholding
# cv2.imshow("ROI", roi)
# cv2.namedWindow('image')
# cv2.createTrackbar('min','image',0,255,nothing)
# cv2.createTrackbar('max','image',0,255,nothing)
# cv2.namedWindow("output")

# while(1):
#   a = cv2.getTrackbarPos('min','image')
#   b = cv2.getTrackbarPos('max','image')
#   ret,thresh=cv2.threshold(roi,a,b,cv2.THRESH_BINARY_INV)
#   clone = thresh;
#   cv2.imshow("output",thresh)
#   k = cv2.waitKey(10) & 0xFF
#   if k == ord("c"):
# 		break

# cv2.waitKey(0)
# cv2.destroyAllWindows()