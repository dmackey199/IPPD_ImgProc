# Source: https://www.thepythoncode.com/article/contour-detection-opencv-python

import cv2
import matplotlib.pyplot as plt

# read the image
image=cv2.imread("circles.png",0)
# convert to RGB
#image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# convert to grayscale
#gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
gray = cv2.medianBlur(img, 5)
# create a binary thresholded image
_, binary = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)
# show it
plt.imshow(binary, cmap="gray")
plt.show()
# find the contours from the thresholded image
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# draw all contours
image = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
# show the image with the drawn contours
plt.imshow(image)
plt.show()