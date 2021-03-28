import cv2
import numpy as np


if __name__ == '__main__':
    # this was only tested on my PC. If running on the pi, you may have to remove the main line and un-indent the code by one tab
    # you may have to play around with these values as where the window is changes
    x = 175
    y = 275
    w = 375
    h = 800
    width = h - y
    height = w - x
    # change the name of the input file here
    cap = cv2.VideoCapture('raw.h264')
    # change the name of the output file here
    out = cv2.VideoWriter('out.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (width, height))
    total = 0
    detected = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            total += 1
            # crop frame
            img = frame[x:w, y:h]
            # circle detecting algorithm
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray_blurred = cv2.blur(gray, (3, 3))
            detected_circles = cv2.HoughCircles(gray_blurred,
                                                cv2.HOUGH_GRADIENT, 1, 20, param1=50,
                                                param2=30, minRadius=1, maxRadius=40)

            # if circles are present, draw them
            if detected_circles is not None:
                detected += 1
                detected_circles = np.uint16(np.around(detected_circles))
                for pt in detected_circles[0, :]:
                    a, b, r = pt[0], pt[1], pt[2]
                    # Draw the circumference of the circle.
                    cv2.circle(img, (a, b), r, (0, 255, 0), 2)
                    # Draw a small circle (of radius 1) to show the center.
                    cv2.circle(img, (a, b), 1, (0, 0, 255), 3)

            # write the frame to video
            out.write(img)
        else:
            # no more frames, exit loop
            break

    # print results
    print('Frames with detected circles: ' + str(detected) + ' of ' + str(total) + ' total frames')
    percent = (detected / total) * 100
    print(str(percent) + '% frames detected circles')
    # close all open objects
    cap.release()
    out.release()
    cv2.destroyAllWindows()
