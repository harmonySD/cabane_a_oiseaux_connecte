#!/usr/bin/python3
import io
import threading, os, signal
import picamera
import logging
import socketserver
from select import select
from threading import Condition
from http import server
import subprocess
from subprocess import check_call, call
import sys
import cv2


ipath = "/home/pi/Projet/blerald-simon-duchatel-2021/code/fluxonline.py"    #CHANGE THIS PATH TO THE LOCATION OF live.py

def thread_second():
    call(["python3", ipath])

def check_kill_process(pstring):
    for line in os.popen("ps ax | grep " + pstring + " | grep -v grep"):
        fields = line.split()
        print(fields)
        pid = fields[0]
        print(pid)
        os.kill(int(pid), signal.SIGKILL)


# run script continuosly
while True:
    # take picture with camera
    print("eejfrefnrjnevk:fsc")
    with picamera.PiCamera() as camera:
        #change resolution to get better latency
        camera.resolution = (640,480)
        camera.capture("/media/pi/4GB DRIVE.jpg")     #CHANGE PATH TO YOUR USB THUMBDRIVE

        # alert picture taken
        print("tic")

            # run live stream again
        processThread = threading.Thread(target=thread_second)
        processThread.start()
        print("Stream running. Refresh page.")

# print in the command line instead of file's consx
if __name__ == '__main__':
    main()