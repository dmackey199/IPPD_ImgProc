#!/usr/bin/env python3

from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image
import PySimpleGUI as sg
import cv2 as cv
import numpy as np

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

sg.theme('BlueMono')   # Add a touch of color
# All the stuff inside your window.
layout1 = [  [sg.Text('Welcome to the Spiny Mouse Selfie!')],
             [sg.Text('Choose a location to backup your data:'), sg.InputText(), sg.FolderBrowse()],
             [sg.Text('If you would like the program to randomize your mice for you, input the number of cages and mice per cage below.')],
            [sg.Text('Otherwise you can choose your order yourself!')],
            [sg.Text('Number of cages:'), sg.InputCombo(['1','2','3'])],
            [sg.Text('Number of mice per cage:'), sg.InputCombo(['1','2','3'])],
            [sg.Button('Randomize for me!'), sg.Button('Let me choose the order!'), sg.Button('Cancel')] ]

layout2 = [ [sg.Text('Place mouse X from cage X into enclosure.')],
            [sg.Text('If trigger did not work. press Start before allowing mouse to eat.')],
            [sg.Button('Start'), sg.Button('Cancel')],
            [sg.Image(filename='', key='image')] ]

layout3 = [ [sg.Text('Mouse ID: '), sg.InputText()],
            [sg.Text('If trigger did not work. press Start before allowing mouse to eat.')],
            [sg.Button('Start'), sg.Button('Cancel')],
            [sg.Image(filename='', key='image')] ]

camera = PiCamera()
rawCap = PiRGBArray(camera)

# need to add start button functionality

# Create the Window
window = sg.Window('Spiny Mouse Selfie', layout1)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':   # if user closes window or clicks cancel
        window.close()
        quit()
    elif event == 'Randomize for me!':
        window.close()
        window = sg.Window('Spiny Mouse Selfie', layout2, finalize=True)
        for frame in camera.capture_continuous(rawCap, format="bgr", use_video_port=True):
            src = frame.array
            #insert image proc algorithm
            resize = ResizeWithAspectRatio(src, height=540)
            imgbytes = cv.imencode('.png', resize)[1].tobytes()
            window['image'].update(data=imgbytes)
            rawCap.truncate(0)
            event1, vals1 = window.read(timeout=1)
            if event1 == sg.WIN_CLOSED or event1 == 'Cancel':
                window.close()
                quit()
    elif event == 'Let me choose the order!':
        window.close()
        window = sg.Window('Spiny Mouse Selfie', layout3, finalize=True)
        for frame in camera.capture_continuous(rawCap, format="bgr", use_video_port=True):
            src = frame.array
            #insert image proc algorithm
            resize = ResizeWithAspectRatio(src, height=540)
            imgbytes = cv.imencode('.png', resize)[1].tobytes()
            window['image'].update(data=imgbytes)
            rawCap.truncate(0)
            event2, vals2 = window.read(timeout=1)
            if event2 == sg.WIN_CLOSED or event2 == 'Cancel':
                window.close()
                quit()
