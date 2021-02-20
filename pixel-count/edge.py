# Source: https://www.thepythoncode.com/article/contour-detection-opencv-python

import cv2
import matplotlib.pyplot as plt

# https://www.pyimagesearch.com/2015/04/20/sorting-contours-using-python-and-opencv/
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


# read the image
#image=cv2.imread("circles.png",0)
# gray=cv2.imread("circles.png",0)
# gray=cv2.imread("img1.png",0)
gray=cv2.imread("img2.png",0)
# convert to RGB
#image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# convert to grayscale
#gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
#gray = cv2.medianBlur(image, 5)
# create a binary thresholded image
_, binary = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
# show it
plt.imshow(binary, cmap="gray")
plt.show()
# find the contours from the thresholded image
contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

sorted_cnts, boundingBoxes = sort_contours(contours, "top-to-bottom")
# print(sorted_cnts[0])

#Show Positions of Objects
x1,y1,w1,h1 = cv2.boundingRect(sorted_cnts[0])
img = cv2.rectangle(gray, (x1, y1), (x1 + w1, y1 + h1), (36,255,12), 1)
cv2.putText(img, 'Reference', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (36,255,12), 1)

x2,y2,w2,h2 = cv2.boundingRect(sorted_cnts[1])
img = cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), (36,255,12), 1)
cv2.putText(img, 'Object', (x2, y2-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (36,255,12), 1)

# draw all contours
image = cv2.drawContours(img, sorted_cnts, -1, (0, 127, 0), 2)
# show the image with the drawn contours
plt.imshow(image)
plt.show()

refArea = cv2.contourArea(sorted_cnts[0])
objArea = cv2.contourArea(sorted_cnts[1])

print "Ref Area: ", refArea
print "Obj Area: ", objArea