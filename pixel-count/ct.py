#intro to color tracking
#https://answers.opencv.org/question/193276/how-to-change-brightness-of-an-image-increase-or-decrease/
#https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html

# hMin = 69
# hMax = 179
# sMin = 40
# sMax = 186
# vMin = 52
# vMax = 158

import cv2
import numpy as np
# import matplotlib.pyplot as plt

def nothing(x):
  pass

img = cv2.imread("img4.png")
hsvImg = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

hsvImg[...,2] = hsvImg[...,2]*0.3

# img = cv2.imread("img4.png")
hsvImg = cv2.fastNlMeansDenoisingColored(hsvImg,None,3,15,7,21)

# cv2.namedWindow('refHole')
# cv2.createTrackbar('min','refHole',0,255,nothing)
# cv2.createTrackbar('max','refHole',0,255,nothing)

# cv2.namedWindow('refHole')
# cv2.createTrackbar('hMin','refHole',0,179,nothing)
# cv2.createTrackbar('hMax','refHole',0,179,nothing)
# cv2.createTrackbar('sMin','refHole',0,255,nothing)
# cv2.createTrackbar('sMax','refHole',0,255,nothing)
# cv2.createTrackbar('vMin','refHole',0,255,nothing)
# cv2.createTrackbar('vMax','refHole',0,255,nothing)
# cv2.namedWindow('hsvImg')
# cv2.namedWindow('mask')

# cv2.namedWindow('refHole')
# cv2.createTrackbar('h','refHole',0,20,nothing)
# cv2.createTrackbar('hColor','refHole',0,20,nothing)

hMin = 69
hMax = 179
sMin = 40
sMax = 186
vMin = 52
vMax = 158
lowerBound = np.array([hMin,sMin,vMin])
upperBound = np.array([hMax,sMax,vMax])
mask = cv2.inRange(hsvImg, lowerBound, upperBound)
invert = cv2.bitwise_not(mask)


cv2.namedWindow('RefThreshold')
while(1):
    # a = cv2.getTrackbarPos('min','refHole')
    # b = cv2.getTrackbarPos('max','refHole')
    # ret,thresh=cv2.threshold(hsvImg,a,b,cv2.THRESH_BINARY_INV)
    # cv2.imshow("RefThreshold",thresh)
    # k = cv2.waitKey(10) & 0xFF
    # if k == ord("c"):
    #     break

    # hMin = cv2.getTrackbarPos('hMin','refHole')
    # hMax = cv2.getTrackbarPos('hMax','refHole')
    # sMin = cv2.getTrackbarPos('sMin','refHole')
    # sMax = cv2.getTrackbarPos('sMax','refHole')
    # vMin = cv2.getTrackbarPos('vMin','refHole')
    # vMax = cv2.getTrackbarPos('vMax','refHole')
    # lowerBound = np.array([hMin,sMin,vMin])
    # upperBound = np.array([hMax,sMax,vMax])
    # mask = cv2.inRange(hsvImg, lowerBound, upperBound)
    # res = cv2.bitwise_and(img,img, mask=mask)
    # cv2.imshow("RefThreshold",res)
    # cv2.imshow("hsvImg",hsvImg)
    # cv2.imshow("mask",mask)
    # k = cv2.waitKey(10) & 0xFF
    # if k == ord("c"):
    #   break

    # h = cv2.getTrackbarPos('h','refHole')
    # hColor = cv2.getTrackbarPos('hColor','refHole')
    # newImg = cv2.fastNlMeansDenoisingColored(hsvImg,None,h,hColor,7,21)
    # cv2.imshow("RefThreshold",newImg)
    # k = cv2.waitKey(10) & 0xFF
    # if k == ord("c"):
    #     break

    cv2.imshow("RefThreshold",invert)
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
cv2.destroyAllWindows()