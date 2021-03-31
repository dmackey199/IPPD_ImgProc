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
from scipy.spatial import distance
# import matplotlib.pyplot as plt

def nothing(x):
  pass

img = cv2.imread("img6.png")
hsvImg = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

hsvImg[...,2] = hsvImg[...,2]*0.7

hsvImg = cv2.fastNlMeansDenoisingColored(hsvImg,None,3,15,7,21)

# cv2.namedWindow('refHole')
# cv2.createTrackbar('min','refHole',0,255,nothing)
# cv2.createTrackbar('max','refHole',0,255,nothing)

cv2.namedWindow('refHole')
cv2.createTrackbar('hMin','refHole',0,179,nothing)
cv2.createTrackbar('hMax','refHole',0,179,nothing)
cv2.createTrackbar('sMin','refHole',0,255,nothing)
cv2.createTrackbar('sMax','refHole',0,255,nothing)
cv2.createTrackbar('vMin','refHole',0,255,nothing)
cv2.createTrackbar('vMax','refHole',0,255,nothing)
cv2.namedWindow('hsvImg')
cv2.namedWindow('mask')

# cv2.namedWindow('refHole')
# cv2.createTrackbar('h','refHole',0,20,nothing)
# cv2.createTrackbar('hColor','refHole',0,20,nothing)

# hMin = 69
# hMax = 179
# sMin = 40
# sMax = 186
# vMin = 52
# vMax = 158
# lowerBound = np.array([hMin,sMin,vMin])
# upperBound = np.array([hMax,sMax,vMax])
# mask = cv2.inRange(hsvImg, lowerBound, upperBound)
# invert = cv2.bitwise_not(mask)
# earContours, earHierarchy = cv2.findContours(invert, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# (h, w) = img.shape[:2]
# image_center = (w//2, h//2)
# # cv2.circle(img, image_center, 3, (255, 100, 0), 2)
# centerCnt = []
# # Sorting by close to center : https://stackoverflow.com/questions/61541559/finding-the-contour-closest-to-image-center-in-opencv2
# for cnt in earContours:
#     # find center of each contour
#     M = cv2.moments(cnt)
#     cX = int(M["m10"] / M["m00"])
#     cY = int(M["m01"] / M["m00"])
#     contour_center = (cX, cY)
#     # calculate distance to image_center
#     distances_to_center = (distance.euclidean(image_center, contour_center))
#     # save to a list of dictionaries
#     centerCnt.append({'contour': cnt, 'center': contour_center, 'distance_to_center': distances_to_center})
#     # draw each contour (red)
#     # cv2.drawContours(img, [cnt], 0, (0, 50, 255), 2)
#     # draw center of contour (green)
#     # cv2.circle(img, contour_center, 3, (100, 255, 0), 2)
#     # sort the buildings
# sorted_cnts = sorted(centerCnt, key=lambda i: i['distance_to_center'])
# # find contour of closest building to center and draw it (blue)
# earHole = sorted_cnts[0]['contour']
# cv2.drawContours(img, [earHole], 0, (255, 0, 0), 2)
# earPixelArea = cv2.contourArea(earHole)
# print("Ear Pixel Area: ", earPixelArea, " pixels")

cv2.namedWindow('RefThreshold')
while(1):
    # a = cv2.getTrackbarPos('min','refHole')
    # b = cv2.getTrackbarPos('max','refHole')
    # ret,thresh=cv2.threshold(hsvImg,a,b,cv2.THRESH_BINARY_INV)
    # cv2.imshow("RefThreshold",thresh)
    # k = cv2.waitKey(10) & 0xFF
    # if k == ord("c"):
    #     break

    hMin = cv2.getTrackbarPos('hMin','refHole')
    hMax = cv2.getTrackbarPos('hMax','refHole')
    sMin = cv2.getTrackbarPos('sMin','refHole')
    sMax = cv2.getTrackbarPos('sMax','refHole')
    vMin = cv2.getTrackbarPos('vMin','refHole')
    vMax = cv2.getTrackbarPos('vMax','refHole')
    lowerBound = np.array([hMin,sMin,vMin])
    upperBound = np.array([hMax,sMax,vMax])
    mask = cv2.inRange(hsvImg, lowerBound, upperBound)
    res = cv2.bitwise_and(img,img, mask=mask)
    cv2.imshow("RefThreshold",res)
    cv2.imshow("hsvImg",hsvImg)
    cv2.imshow("mask",mask)
    k = cv2.waitKey(10) & 0xFF
    if k == ord("c"):
      break

    # h = cv2.getTrackbarPos('h','refHole')
    # hColor = cv2.getTrackbarPos('hColor','refHole')
    # newImg = cv2.fastNlMeansDenoisingColored(hsvImg,None,h,hColor,7,21)
    # cv2.imshow("RefThreshold",newImg)
    # k = cv2.waitKey(10) & 0xFF
    # if k == ord("c"):
    #     break

    # cv2.imshow("hsvImg",hsvImg)
    # cv2.imshow("RefThreshold",img)
    # k = cv2.waitKey(10) & 0xFF
    # if k == ord("c"):
    #   break


cv2.destroyAllWindows()