import numpy as np
import cv2
import matplotlib.pyplot as plt

staticCrop = [(151, 62), (581, 173)] 
greedyCrop = [(177, 60), (281, 147)]

actualArea = 8.0

def nothing(x):
  pass


# image = cv2.imread("img1.png")
# alpha = 1.3;
# beta = 20;
# new_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

# cv2.imshow('Original Image', image)
# cv2.imshow('New Image', new_image)
# # Wait until user press some key
# cv2.waitKey()











# roi = cv2.imread("img2.png")
# gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
# clone = gray.copy()
# #roi = clone[staticCrop[0][1]:staticCrop[1][1], staticCrop[0][0]:staticCrop[1][0]]
# roi = clone[greedyCrop[0][1]:greedyCrop[1][1], greedyCrop[0][0]:greedyCrop[1][0]]

# cv2.imshow("ROI", roi)
# cv2.waitKey(0)

# # HoughCircles
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


def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)

og = cv2.imread("img2.png")
gray = cv2.cvtColor(og, cv2.COLOR_BGR2GRAY)
clone = gray.copy()
#roi = clone[staticCrop[0][1]:staticCrop[1][1], staticCrop[0][0]:staticCrop[1][0]]
roi = clone[greedyCrop[0][1]:greedyCrop[1][1], greedyCrop[0][0]:greedyCrop[1][0]]
alpha = 1.2;
beta = 10;
output = cv2.convertScaleAbs(roi, alpha=alpha, beta=beta)

# cv2.imshow("og", og)
# cv2.imshow("Output", output)

# cv2.waitKey(0)

low = 32
high = 179
edges = cv2.Canny(output, low, high)

contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
print "Contours found: ", len(contours)
if len(contours) <= 1 :
	print("Unable to detect 2 contours!")
if len(contours) >= 3 :
	print("Detecting more than 2 contours!")

sorted_cnts, boundingBoxes = sort_contours(contours, "bottom-to-top")
#Show Positions of Objects
x1,y1,w1,h1 = cv2.boundingRect(sorted_cnts[0])
img = cv2.rectangle(output, (x1, y1), (x1 + w1, y1 + h1), (36,255,12), 1)
cv2.putText(img, 'Object', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (36,255,12), 1)

x2,y2,w2,h2 = cv2.boundingRect(sorted_cnts[1])
img = cv2.rectangle(output, (x2, y2), (x2 + w2, y2 + h2), (255,36,12), 1)

# draw all contours
image = cv2.drawContours(output, sorted_cnts, -1, (0, 127, 0), 2)
# show the image with the drawn contours
plt.imshow(image)
plt.show()

objArea = cv2.contourArea(sorted_cnts[0])
refArea = cv2.contourArea(sorted_cnts[1])
print(objArea)
print(refArea)

areaPerPixel = actualArea / refArea
calculatedArea = objArea * areaPerPixel

print(calculatedArea)




#thresholding
# roi = cv2.imread("img2.png")
# gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
# clone = gray.copy()
# #roi = clone[staticCrop[0][1]:staticCrop[1][1], staticCrop[0][0]:staticCrop[1][0]]
# roi = clone[greedyCrop[0][1]:greedyCrop[1][1], greedyCrop[0][0]:greedyCrop[1][0]]
# alpha = 1.2;
# beta = 10;
# output = cv2.convertScaleAbs(roi, alpha=alpha, beta=beta)


# cv2.imshow("ROI", output)
# cv2.namedWindow('image')
# cv2.createTrackbar('min','image',0,255,nothing)
# cv2.createTrackbar('max','image',0,255,nothing)
# cv2.namedWindow("output")

# while(1):
#   a = cv2.getTrackbarPos('min','image')
#   b = cv2.getTrackbarPos('max','image')
#   # ret,thresh=cv2.threshold(output,a,b,cv2.THRESH_BINARY_INV)
#   edges = cv2.Canny(output, a, b)
#   # clone = thresh;
#   cv2.imshow("output",edges)
#   #cv2.imshow("output",thresh)
#   k = cv2.waitKey(10) & 0xFF
#   if k == ord("c"):
# 		break

# cv2.waitKey(0)
# cv2.destroyAllWindows()