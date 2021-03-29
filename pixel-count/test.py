import numpy as np
import cv2
import argparse
import math

#4mm hole has radius of 2, Area = pi * r^2
refArea = (2**2) * math.pi
refPt = []
initCrop = []
roi = cv2.imread("img3.png",0)
# x1, y1


#                             x2,y2
def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, initCrop, roi
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
            initCrop = [(x,y)]
		# refPt = [(x, y)]
	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
            initCrop.append((x,y))
            x1 = min(initCrop[0][0], initCrop[1][0])
            x2 = max(initCrop[0][0], initCrop[1][0])
            y1 = min(initCrop[0][1], initCrop[1][1])
            y2 = max(initCrop[0][1], initCrop[1][1])
            refPt = [(x1,y1)]
            refPt.append((x2, y2))
		# draw a rectangle around the region of interest
            cv2.rectangle(roi, refPt[0], refPt[1], (255, 255, 255), 2)

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

#START
img = cv2.imread("img3.png",0)
clone = img.copy()

def nothing(x):
  pass

cv2.namedWindow("output")
cv2.setMouseCallback("output", click_and_crop)

while(1):

  cv2.imshow("output",img)
  k = cv2.waitKey(10) & 0xFF
	# if the 'c' key is pressed, break from the loop
  if k == ord("c"):
		break


if len(refPt) == 2:
  roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
  print("Crop points: ",refPt)
  cv2.imshow("ROI", roi)
  while(1):
    k = cv2.waitKey(10) & 0xFF
    if k == ord("c"):
		break

cv2.destroyAllWindows()

cv2.namedWindow('image')
cv2.createTrackbar('min','image',0,255,nothing)
cv2.createTrackbar('max','image',0,255,nothing)

cv2.namedWindow('Threshold')
while(1):

    a = cv2.getTrackbarPos('min','image')
    b = cv2.getTrackbarPos('max','image')
    ret,thresh=cv2.threshold(roi,a,b,cv2.THRESH_BINARY_INV)
    cv2.imshow("Threshold",thresh)
    k = cv2.waitKey(10) & 0xFF
    if k == ord("c"):
		  break

# cv2.namedWindow('Threshold')
# while(1):
#     ret,thresh=cv2.threshold(roi,80,255,cv2.THRESH_BINARY_INV)
#     cv2.imshow("Threshold",thresh)
#     k = cv2.waitKey(10) & 0xFF
#     if k == ord("c"):
#         break

# def find_thresh(img, val):
#   cv2.namedWindow('Threshold')
#   while(1):
#       ret,thresh=cv2.threshold(img,val,255,cv2.THRESH_BINARY_INV)
#       cv2.imshow("Threshold",thresh)
#       k = cv2.waitKey(10) & 0xFF
#       if k == ord("c"):
#           break
#   return thresh

# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

chosen_contours = []
# thresh = None
# thresh_val = 70
# while(thresh_val < 120):
#   thresh = find_thresh(roi, thresh_val)
#   contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#   if(len(contours) != 0):
#     print("Curr Thresh: ", thresh_val)
#     print("Len: ", len(contours))
#     for i in range(len(contours)):
#         area = cv2.contourArea(contours[i])
#         if(area > 1000 and area < 2000):
#             chosen_contours.append(contours[i])
#             print("Contour Area: ", area)
#     if(len(chosen_contours) != 0): # if good contours were found
#       break
#     thresh_val += 10
#     print("New Thresh: ", thresh_val)
        # x1,y1,w1,h1 = cv2.boundingRect(contours[i])
        # rect = cv2.rectangle(roi, (x1, y1), (x1 + w1, y1 + h1), (36,255,12), 1)
        # cv2.putText(rect, "EYE", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (36,255,12), 1)

# if(len(chosen_contours) == 0):
#   print("No Contours found!")

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.namedWindow('Contours')
for i in range(len(contours)):
    area = cv2.contourArea(contours[i])
    if(area > 1500 and area < 3000):
        chosen_contours.append(contours[i])
if(len(chosen_contours) == 0):
  print("No Contours found!")
sorted_contours, boundingBoxes = sort_contours(chosen_contours, "top-to-bottom")
print(cv2.contourArea(sorted_contours[0]))
x,y,w,h = cv2.boundingRect(sorted_contours[0])

earCrop = [(x-250,y-50), (x-170, y + h/2)]
refCrop = [(5,5), (150,150)]

# sorted_contours, boundingBoxes = sort_contours(chosen_contours, "top-to-bottom")
# x,y,w,h = cv2.boundingRect(sorted_contours[0])

rect = cv2.rectangle(roi, (x, y), (x + w, y + h), (36,255,12), 1)
cv2.putText(rect, "EYE", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (36,255,12), 1)

rect = cv2.rectangle(roi, (5,5), (80,80), (36,255,12), 1)
cv2.putText(rect, "Reference", (10, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1, (36,255,12), 1)

rect = cv2.rectangle(roi, (x-120,y-50), ((x -80), y + (h/2)), (36,255,12), 1)
cv2.putText(rect, "Ear", (x-250, y + h), cv2.FONT_HERSHEY_SIMPLEX, 1, (36,255,12), 1)

image = cv2.drawContours(roi, sorted_contours, -1, (0, 127, 0), 2)
# show the image with the drawn contours
while(1):
    cv2.imshow("Contours",image)
    k = cv2.waitKey(10) & 0xFF
    if k == ord("c"):
        break

#print("Contours found: ", len(sorted_contours))

earPic = roi[earCrop[0][1]:earCrop[1][1], earCrop[0][0]:earCrop[1][0]]
refPic = roi[refCrop[0][1]:refCrop[1][1], refCrop[0][0]:refCrop[1][0]]



cv2.namedWindow('ear')
# while(1):
#   cv2.imshow("ear",earPic)
#   k = cv2.waitKey(10) & 0xFF
#   if k == ord("c"):
#     break

cv2.createTrackbar('min','ear',0,255,nothing)
cv2.createTrackbar('max','ear',0,255,nothing)

cv2.namedWindow('EarThreshold')
while(1):

    a = cv2.getTrackbarPos('min','ear')
    b = cv2.getTrackbarPos('max','ear')
    # ret,thresh=cv2.threshold(earPic,a,b,cv2.THRESH_BINARY_INV)
    # cv2.imshow("EarThreshold",thresh)
    edges=cv2.Canny(earPic,a,b)
    cv2.imshow("EarThreshold",edges)
    k = cv2.waitKey(10) & 0xFF
    if k == ord("c"):
		  break

cv2.destroyAllWindows()


# cv2.namedWindow('refHole')
# while(1):
#   cv2.imshow("ear",refPic)
#   k = cv2.waitKey(10) & 0xFF
#   if k == ord("c"):
#     break
# cv2.createTrackbar('min','refHole',0,255,nothing)
# cv2.createTrackbar('max','refHole',0,255,nothing)

# cv2.namedWindow('RefThreshold')
# while(1):

#     a = cv2.getTrackbarPos('min','refHole')
#     b = cv2.getTrackbarPos('max','refHole')
#     ret,thresh=cv2.threshold(refPic,a,b,cv2.THRESH_BINARY_INV)
#     cv2.imshow("RefThreshold",thresh)
#     k = cv2.waitKey(10) & 0xFF
#     if k == ord("c"):
# 		  break
# cv2.namedWindow('RefThreshold')
ret,refThresh=cv2.threshold(refPic,167,255,cv2.THRESH_BINARY_INV)
refContours, refHierarchy = cv2.findContours(refThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

refPixelArea = 0
for i in range(len(refContours)):
    area = cv2.contourArea(refContours[i])
    if(area > 100):
        refContours = refContours[i]
        refPixelArea = area
        break
print("Contours found: ", len(refContours))

refx,refy,refw,refh = cv2.boundingRect(refContours)
rect = cv2.rectangle(refPic, (refx, refy), (refx + refw, refy + refh), (36,255,12), 1)
cv2.putText(rect, "REF", (refx, refy+refh+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (36,255,12), 1)
newRefPic = cv2.drawContours(refPic, refContours, -1, (0, 127, 0), 2)
cv2.namedWindow('RefContours')
# show the image with the drawn contours
while(1):
    cv2.imshow("RefContours",newRefPic)
    k = cv2.waitKey(10) & 0xFF
    if k == ord("c"):
        break

print("Actual Area of Ref Circle: ", refArea)
print("Pixel Area of Ref Circle: ", refPixelArea)
cv2.destroyAllWindows()