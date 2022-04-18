#!/usr/bin/python3
import io
import threading, os, signal
from time import time
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
import time


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
i=0
begin_time= time.localtime(time.time())
while i==0:
    # take picture with camera
    now= time.localtime(time.time())
    if((int(time.strftime("%S",begin_time))+40<int(time.strftime("%S",now)) )or (int(time.strftime("%M",begin_time))<int(time.strftime("%M",now)))):
        begin_time=time.localtime(time.time())
        i+=1
        check_kill_process('fluxonline.py')
        print("Stream ended.")
        with picamera.PiCamera() as camera:
            #change resolution to get better latency
            camera.resolution = (640,480)
            camera.capture("/home/pi/Projet/blerald-simon-duchatel-2021/code/img.jpg")     #CHANGE PATH TO YOUR USB THUMBDRIVE

            # alert picture taken
            print("tic")

                # run live stream again
            processThread = threading.Thread(target=thread_second)
            processThread.start()
            print("Stream running. Refresh page.")

# print in the command line instead of file's consx
if __name__ == '__main__':
    main()