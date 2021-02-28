#!/usr/bin/env python3

from picamera import PiCamera
from PIL import Image
from time import sleep
from datetime import datetime
import pickle
import PySimpleGUI as sg
import cv2 as cv
import numpy as np
import RPi.GPIO as GPIO
import shutil

mouseid = ""
backup = ""

sg.theme('BlueMono')   # Add a touch of color
# All the stuff inside your window.
layout1 = [  [sg.Text('Welcome to the Spiny Mouse Selfie!')],
             [sg.Text('Please preview the camera to make sure the picture is clear')],
             [sg.Button('Preview Camera')],
            [sg.Text('Mouse ID: '), sg.InputText(mouseid)],
             [sg.Text('Choose a location to backup your data:'), sg.InputText(backup), sg.FolderBrowse()],
            [sg.Text('Press begin to begin')],
            [sg.Button('Begin'), sg.Button('Cancel')] ]

layout2 = [  [sg.Text('The trigger will start the image process')]]

layout = [[sg.Column(layout1, key='lay1'), sg.Column(layout2, visible=False, key='lay2')]]

camera = PiCamera()
camera.framerate = 100

# need to add start button functionality

# Create the Window
window = sg.Window('Spiny Mouse Selfie', layout, finalize=True)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    mouseid = ""
    window.FindElement('lay1').update(visible=True)
    window.FindElement('lay2').update(visible=False)
    window.Refresh()
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':   # if user closes window or clicks cancel
        window.close()
        camera.close()
        quit()
    elif event == 'Preview Camera':
        camera.start_preview()
        sleep(30)
        camera.stop_preview()
    elif event == 'Begin':
        mouseid = values[0]
        backup = values[1]
        window.FindElement('lay1').update(visible=False)
        window.FindElement('lay2').update(visible=True)
        window.Refresh()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23, GPIO.IN, GPIO.PUD_UP)
        trigger = GPIO.input(23)
        while trigger == 1:
            trigger = GPIO.input(23)
            print("wait")
        # start image processing and save it
        print("reached")
        now = datetime.now().strftime("H%H-M%M-S%S")
        name = "id-" + mouseid + "-" + now + ".h264"
        camera.start_preview()
        camera.start_recording(name, format='h264')
        sleep(10)
        camera.stop_recording()
        camera.stop_preview()
        fcopy = backup + "/" + name
        shutil.copyfile(name, fcopy)
