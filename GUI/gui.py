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

mouseid = ""
backup = ""
secs = ""
testsec = ""

sg.theme('BlueMono')   # Add a touch of color
# All the stuff inside your window.
test_frame = [ [sg.Text('Here you can test the focus of the Camera and the IR Beams!', font=("Helvetica",12))],
               [sg.Text('If you are testing the IR Beams, please select "execute in terminal" upon start.', font=("Helvetica",12))],
            [sg.Text('Test time (in seconds):', font=("Helvetica",12)), sg.InputText(testsec)],
            [sg.Text('Camera Frame Rate:', font=("Helvetica",12)), sg.Radio('90', "fr", default=True, font=("Helvetica",12)), sg.Radio('60', "fr", font=("Helvetica",12)), sg.Radio('30', "fr", font=("Helvetica",12))],
             [sg.Button('Preview Camera', font=("Helvetica",12)), sg.Button('Test Left IR Beam', font=("Helvetica",12)), sg.Button('Test Right IR Beam', font=("Helvetica",12))] ]

data_frame = [ [sg.Text('Please enter the animal ID, backup location, and direction.', font=("Helvetica",12))],
               [sg.Text('By selecting "Begin with Beams", the IR Beams will be used to start the video recording.', font=("Helvetica",12))],
               [sg.Text('If Beams are unavailable, please enter how long the video should record and select "Begin without Beams".', font=("Helvetica",12))],
                [sg.Text('Animal ID:', font=("Helvetica",12)), sg.InputText(mouseid)],
              [sg.Text('Data Backup Location:', font=("Helvetica",12)), sg.InputText(backup), sg.FolderBrowse(font=("Helvetica",12))],
            [sg.Text('The mouse is entering from the:', font=("Helvetica",12)), sg.Radio('Left', "direction", default=True, font=("Helvetica",12)), sg.Radio('Right', "direction", font=("Helvetica",12))],
            [sg.Text('Recording time in seconds (if Beams are unavailable):', font=("Helvetica",12)), sg.InputText(secs)],
            [sg.Button('Begin with Beams', font=("Helvetica",12)), sg.Button('Begin without Beams', font=("Helvetica",12))] ]

col = [ [sg.Text('Welcome to the Spiny Mouse Selfie!', font=("Helvetica",25) )],
            [sg.Frame('Testing', test_frame, title_color='blue', font=("Helvetica",12))] ]

layout1 = [ [sg.Column(col), sg.Image(r'placeholderlogo.png')],
            [sg.Frame('Data Collection', data_frame, title_color='blue', font=("Helvetica",12))] ]

layout2 = [  [sg.Text('The trigger will start the measuring process.', font=("Helvetica",16))]]

layout3 = [  [sg.Text('Please check the terminal to see the output. The program will return to the main screen after the specified time.', font=("Helvetica",16))]]

layout = [[sg.Column(layout1, key='lay1'), sg.Column(layout2, visible=False, key='lay2'), sg.Column(layout3, visible=False, key='lay3')]]

# need to add start button functionality

# Create the Window
window = sg.Window('Spiny Mouse Selfie', layout, finalize=True)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    mouseid = ""
    window.FindElement('lay1').update(visible=True)
    window.FindElement('lay2').update(visible=False)
    window.FindElement('lay3').update(visible=False)
    window.Refresh()
    event, values = window.Read()
    print(values)
    if values[1]:
        camera.resolution = (640,480) #90fps
        camera.framerate = 90
    elif values[2]:
        camera.resolution = (1280,720) #60fps
        camera.framerate = 60
    else:
        camera.resolution = (1920,1080) #30fps
        camera.framerate = 30
    if event == sg.WIN_CLOSED:   # if user closes window or clicks cancel
        window.close()
        camera.close()
        quit()
    elif event == 'Preview Camera':
        camera.start_preview()
        sleep(int(values[0]))
        camera.stop_preview()
    elif event == 'Test Left IR Beam':
        window.FindElement('lay1').update(visible=False)
        window.FindElement('lay2').update(visible=False)
        window.FindElement('lay3').update(visible=True)
        window.Refresh()
        loops = 0
        while (float(loops) * 0.05) < int(values[0]):
            i=GPIO.input(23)
            if i==1:                 #When output from motion sensor is LOW
                print("No Object")
                time.sleep(0.05)
            elif i==0:               #When output from motion sensor is HIGH
                print("Object detected")
                time.sleep(0.05)
            loops += 1
    elif event == 'Test Right IR Beam':
        window.FindElement('lay1').update(visible=False)
        window.FindElement('lay2').update(visible=False)
        window.FindElement('lay3').update(visible=True)
        window.Refresh()
        loops = 0
        while (float(loops) * 0.05) < int(values[0]):
            i=GPIO.input(24)
            if i==1:                 #When output from motion sensor is LOW
                print("No Object")
                time.sleep(0.05)
            elif i==0:               #When output from motion sensor is HIGH
                print("Object detected")
                time.sleep(0.05)
            loops += 1
    elif event == 'Begin with Beams':
        print(values)
        mouseid = values[5]
        backup = values[6]
        window.FindElement('lay1').update(visible=False)
        window.FindElement('lay2').update(visible=True)
        window.FindElement('lay3').update(visible=False)
        window.Refresh()
        start = 0
        end = 0
        if values[7]:
            start = 23
            end = 24
        elif values[8]:
            start = 24
            end = 23
        trigger = GPIO.input(start)
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
    elif event == 'Begin without Beams':
        print(values)
        mouseid = values[5]
        backup = values[6]
        secs = values[9]
        window.FindElement('lay1').update(visible=False)
        window.FindElement('lay2').update(visible=False)
        window.FindElement('lay3').update(visible=False)
        window.Refresh()
        now = datetime.now().strftime("H%H-M%M-S%S")
        name = "id-" + str(mouseid) + "-" + now + ".h264"
        camera.start_preview()
        camera.start_recording(name, format='h264')
        time.sleep(int(secs))
        camera.stop_recording()
        camera.stop_preview()
        fcopy = backup + "/" + name
        shutil.copyfile(name, fcopy)
