import numpy as np
import cv2

staticCrop = [(151, 62), (581, 173)] 
greedyCrop = [(177, 60), (281, 147)]

roi = cv2.imread("img1.png",0)
clone = roi.copy()
roi = clone[staticCrop[0][1]:staticCrop[1][1], staticCrop[0][0]:staticCrop[1][0]]
cv2.imshow("ROI", roi)
cv2.waitKey(0)
cv2.destroyAllWindows()