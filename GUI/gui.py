#!/usr/bin/env python3

import pickle
import PySimpleGUI as sg
import cv2 as cv
import numpy as np
import RPi.GPIO as GPIO
import shutil
import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from PIL import Image
from time import sleep
from datetime import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, GPIO.PUD_UP)

camera = PiCamera()
camera.framerate = 90

mouseid = ""
backup = ""
direction = ""

sg.theme('BlueMono')   # Add a touch of color
# All the stuff inside your window.
test_frame = [ [sg.Text('Please preview the camera to make sure the picture is clear')],
             [sg.Button('Preview Camera'), sg.Button('Test Left IR Beam'), sg.Button('Test Right IR Beam')] ]

data_frame = [ [sg.Text('Directions will go here')],
                [sg.Text('Mouse ID: '), sg.InputText(mouseid)],
              [sg.Text('Data Backup Location:'), sg.InputText(backup), sg.FolderBrowse()],
            [sg.Text('The mouse is entering from the:'), sg.Combo(['Left', 'Right'])],
            [sg.Text('Press begin to begin')],
            [sg.Button('Begin'), sg.Button('Cancel')] ]

col = [ [sg.Text('Welcome to the Spiny Mouse Selfie!', font=("Helvetica",25) )],
            [sg.Frame('Testing', test_frame, title_color='blue')] ]

layout1 = [ [sg.Column(col), sg.Image(r'placeholderlogo.png')],
            [sg.Frame('Data Collection', data_frame, title_color='blue')] ]

# layout1 = [ [sg.Text('Please preview the camera to make sure the picture is clear')],
#              [sg.Button('Preview Camera'), sg.Button('Test Left IR Beam'), sg.Button('Test Right IR Beam')],
#             [sg.Text('Directions will go here')],
#                 [sg.Text('Mouse ID: '), sg.InputText(mouseid)],
#               [sg.Text('Data Backup Location:'), sg.InputText(backup), sg.FolderBrowse()],
#             [sg.Text('The mouse is entering from the:'), sg.Combo(['Left', 'Right'])],
#             [sg.Text('Press begin to begin')],
#             [sg.Button('Begin'), sg.Button('Cancel')] ]

layout2 = [  [sg.Text('The trigger will start the image process')]]

layout3 = [  [sg.Text('Check terminal to see output. Exit program and reopen to return to home menu')]]

layout = [[sg.Column(layout1, key='lay1'), sg.Column(layout2, visible=False, key='lay2'), sg.Column(layout3, visible=False, key='lay3')]]

# need to add start button functionality

# Create the Window
window = sg.Window('Spiny Mouse Selfie', layout, finalize=True)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    mouseid = ""
    window.FindElement('lay1').update(visible=True)
    window.FindElement('lay2').update(visible=False)
    window.Refresh()
    event, values = window.Read()
    if event == sg.WIN_CLOSED or event == 'Cancel':   # if user closes window or clicks cancel
        window.close()
        camera.close()
        quit()
    elif event == 'Preview Camera':
        camera.start_preview()
        sleep(30)
        camera.stop_preview()
    elif event == 'Test Left IR Beam':
        window.FindElement('lay1').update(visible=False)
        window.FindElement('lay3').update(visible=True)
        window.Refresh()
        while True:
            i=GPIO.input(23)
            if i==1:                 #When output from motion sensor is LOW
                print("No Object")
                time.sleep(0.05)
            elif i==0:               #When output from motion sensor is HIGH
                print("Object detected")
                time.sleep(0.05)
    elif event == 'Test Right IR Beam':
        window.FindElement('lay1').update(visible=False)
        window.FindElement('lay3').update(visible=True)
        window.Refresh()
        while True:
            i=GPIO.input(24)
            if i==1:                 #When output from motion sensor is LOW
                print("No Object")
                time.sleep(0.05)
            elif i==0:               #When output from motion sensor is HIGH
                print("Object detected")
                time.sleep(0.05)
    elif event == 'Begin':
        mouseid = values[1]
        backup = values[2]
        direction = values[3]
        window.FindElement('lay1').update(visible=False)
        window.FindElement('lay2').update(visible=True)
        window.Refresh()
        if direction == "Left":
            start = 23
            end = 24
        elif direction == "Right":
            start = 24
            end = 23
        trigger = GPIO.input(start)
        print(start)
        while trigger == 1:
            trigger = GPIO.input(start)
        now = datetime.now().strftime("H%H-M%M-S%S")
        name = "id-" + str(mouseid) + "-" + now + ".h264"
        camera.start_preview()
        camera.start_recording(name, format='h264')
        trigger = GPIO.input(end)
        while trigger == 1:
            trigger = GPIO.input(end)
        camera.stop_recording()
        camera.stop_preview()
        fcopy = backup + "/" + name
        shutil.copyfile(name, fcopy)
