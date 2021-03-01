import cv2
import numpy as np

img = cv2.imread("mouseimg.png")
# cv2.imshow("original", img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow("gray", gray)

blur = cv2.medianBlur(gray, 31)
# cv2.imshow("blur", blur)

ret, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_OTSU)
# cv2.imshow("thresh", thresh)

canny = cv2.Canny(thresh, 75, 200)
# cv2.imshow('canny', canny)

contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

contour_list = []
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
    area = cv2.contourArea(contour)
    if area < 500:
        contour_list.append(contour)

for cnt in contour_list:
    print(cv2.contourArea(cnt))

msg = "Total holes: {}".format(len(approx)//2)
cv2.putText(img, msg, (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)

cv2.drawContours(img, contour_list, -1, (0, 255, 0), 2)
cv2.imshow('Objects Detected', img)

cv2.imwrite("detected_holes.png", img)

cv2.waitKey(0)