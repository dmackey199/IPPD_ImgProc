#Courtesy of https://stackoverflow.com/questions/45836214/opencv-python-count-pixels

import numpy as np
import cv2

# def ResizeWithAspectRatio(image, width=None, height=None, inter=cv.INTER_AREA):
#     dim = None
#     (h, w) = image.shape[:2]

#     if width is None and height is None:
#         return image
#     if width is None:
#         r = height / float(h)
#         dim = (int(w * r), height)
#     else:
#         r = width / float(w)
#         dim = (width, int(h * r))

#     return cv.resize(image, dim, interpolation=inter)

# ap = argparse.ArgumentParser()
# ap.add_argument("-w", "--width", type=float, required=True,
#     help="width of the left-most object in the image (in inches)")
# args = vars(ap.parse_args())


    # src = frame.array

    # ## [convert_to_gray]
    # # Convert it to gray
    # gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    # ## [convert_to_gray]

    # ## [reduce_noise]
    # # Reduce the noise to avoid false circle detection
    # gray = cv.medianBlur(gray, 5)
    # ## [reduce_noise]

    # ## [houghcircles]
    # rows = gray.shape[0]
    # circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 8,
    #                            param1=100, param2=30,
    #                            minRadius=0, maxRadius=30)
    # ## [houghcircles]
    
    # pixelsPerMetric = None

    # ## [draw]
    # unknown = False 
    # if circles is not None:
    #     circles = np.uint16(np.around(circles))
    #     if len(circles[0, :]) == 2:
    #         if circles[0][0][1] > circles[0][1][1]:
    #             temp = np.copy(circles[0][0])
    #             circles[0][0] = circles[0][1]
    #             circles[0][1] = temp
    #         for i in circles[0, :]:
    #             if pixelsPerMetric is None:
    #                 pixelsPerMetric = i[2] / args["width"]
                    
    #             center = (i[0], i[1])
    #             # circle outline
    #             size = i[2] / pixelsPerMetric
    #             if (unknown):
    #                 measurements.append(size)
    #                 times.append(datetime.now().strftime("%H:%M:%S"))
    #             else:
    #                 unknown = True

    #             cv.circle(src, center, i[2], (255, 0, 255), 3)
    #             cv.putText(src, "{:.2f}mm".format(size),
    #                 center, cv.FONT_HERSHEY_TRIPLEX,
    #                 2, (10, 202, 55), 2)
    #         resize = ResizeWithAspectRatio(src, height=540)
    #         filename = 'Image' + str(a) + '-Mouse' + args["id"] + '.jpg'
    #         a = a + 1
    #         cv.imwrite(filename, resize)
            
    # resize = ResizeWithAspectRatio(src, height=540)
    # cv.imshow("Frame", resize)
    # key = cv.waitKey(1) & 0xFF
    # rawCap.truncate(0)

##

img=cv2.imread("box.png",0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def nothing(x):
  pass

cv2.namedWindow('image')

cv2.createTrackbar('min','image',0,255,nothing)
cv2.createTrackbar('max','image',0,255,nothing)

while(1):

 a = cv2.getTrackbarPos('min','image')
 b = cv2.getTrackbarPos('max','image')
 ret,thresh=cv2.threshold(img,a,b,cv2.THRESH_BINARY_INV)
 cv2.imshow("output",thresh)
 k = cv2.waitKey(10) & 0xFF
 if k == 27:
    break
print "Pixel Count: " + cv2.countNonZero(thresh)
print "Area is mm"
cv2.destroyAllWindows()