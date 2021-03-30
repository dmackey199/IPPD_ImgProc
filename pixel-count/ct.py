#intro to color tracking
#https://answers.opencv.org/question/193276/how-to-change-brightness-of-an-image-increase-or-decrease/
#https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html

import cv2
import numpy as np
# import matplotlib.pyplot as plt

def nothing(x):
  pass

img = cv2.imread("img5.png")
hsvImg = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

hsvImg[...,2] = hsvImg[...,2]*0.7

cv2.namedWindow('refHole')
cv2.createTrackbar('min','refHole',0,255,nothing)
cv2.createTrackbar('max','refHole',0,255,nothing)
cv2.namedWindow('RefThreshold')
while(1):
    a = cv2.getTrackbarPos('min','refHole')
    b = cv2.getTrackbarPos('max','refHole')
    ret,thresh=cv2.threshold(hsvImg,a,b,cv2.THRESH_BINARY_INV)
    cv2.imshow("RefThreshold",thresh)
    # cv2.imshow("RefThreshold",hsvImg)
    k = cv2.waitKey(10) & 0xFF
    if k == ord("c"):
      break

# plt.subplot(111), plt.imshow(cv2.cvtColor(hsvImg,cv2.COLOR_HSV2RGB))
# plt.title('brightened image'), plt.xticks([]), plt.yticks([])
# plt.show()

# white = np.uint8([[[255,255,255 ]]])
# white = np.uint8([[[0,255,0]]])
# hsv_white = cv2.cvtColor(white,cv2.COLOR_BGR2HSV)
# print(hsv_white)

# Convert BGR to HSV
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# # define range of blue color in HSV
# lower_blue = np.array([0,50,50])
# upper_blue = np.array([20,255,255])

# # Threshold the HSV image to get only blue colors
# mask = cv2.inRange(hsv, lower_blue, upper_blue)

# # Bitwise-AND mask and original image
# res = cv2.bitwise_and(hsv,hsv, mask= mask)

# plt.subplot(111), plt.imshow(cv2.cvtColor(res,cv2.COLOR_HSV2RGB))
# plt.title('brightened image'), plt.xticks([]), plt.yticks([])
# plt.show()

# cv2.namedWindow('hsv')
# cv2.namedWindow('mask')
# cv2.namedWindow('res')
# while(1):
#     # cv2.imshow('hsv',hsv)
#     # cv2.imshow('mask',mask)
#     cv2.imshow('res',res)
#     k = cv2.waitKey(5) & 0xFF
#     if k == ord("c"):
#         break
# cv2.destroyAllWindows()