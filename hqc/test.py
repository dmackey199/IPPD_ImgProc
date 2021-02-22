from picamera import PiCamera
from time import sleep
import cv2 as cv
import argparse

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv.resize(image, dim, interpolation=inter)

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", type=str, required=True,
    help="name of vid file")
args = vars(ap.parse_args())

vid = cv.VideoCapture(args["name"])

while (vid.isOpened()):
    ret, src = vid.read()
    print(ret)
    resize = ResizeWithAspectRatio(src, height=540)
    cv.imshow("Frame", resize)
    if cv.waitKey(1) & 0xFF == ord('q'):
         break