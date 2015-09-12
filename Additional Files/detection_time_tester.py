# -*- coding: utf-8 -*-
import commandMenu
import io
import picamera
import cv2
import cv
import time
import HandDetectValidator
from HandDetection import handDetect
import HandDetection
import picamera.array
import numpy as np
import pygame




if __name__ == '__main__':
    pygame.mixer.init()
    global rbeep , lbeep
    rbeep= pygame.mixer.Sound('./beep_right.wav')
    lbeep= pygame.mixer.Sound('./beep_left.wav')
    
    hand_cascade = cv2.CascadeClassifier('cascadeMT.xml')

    RH_DET_THRESH = 3 # number of times it must be detected consecutively
    LH_DET_THRESH = 1 # number of times it must be detected consecutively    
    MAX_NUM_LEFT_ATTMEPTS = 3
    MAXDIST = 10
    RESIZE_FULL_RES_FACTOR = 5
    rhValidator = HandDetectValidator.HandDetectValidator(MAXDIST , RH_DET_THRESH)
    lhValidator = HandDetectValidator.HandDetectValidator(MAXDIST , LH_DET_THRESH)
    
    detectRight = True # If false, will detect left hands
    numLeftAttempts = 0
    resFile = open('res.txt','w')
    rejectLevels =[]
    levelWeights = []
    with picamera.PiCamera() as camera:
        fullResStream = picamera.array.PiRGBArray(camera)
        with picamera.array.PiRGBArray(camera) as stream:
            camera.resolution = (160,120)
            #i = 0
            fr = 1
            
            camera.capture(stream, format='bgr' , use_video_port = True)
                
                # At this point the image is available as stream.array
            image = stream.array
                #rotate image
                #image=image[::-1,::-1]
            sf = 1.01
            step = 0.05
            
            for i in range(45):
                print 'testing sf ',sf
                sum = 0.0
                for t in range(10):
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    start = time.time()
                    hands = hand_cascade.detectMultiScale(gray,rejectLevels,levelWeights, sf, 5,cv.CV_HAAR_FIND_BIGGEST_OBJECT,(30, 30),(60,60),True)
                    end = time.time()
                    elapsed = end - start
                    sum += elapsed
                avg = sum / 10
                resFile.write(str(sf)+','+str(avg)+'\n')
                sf += step

                    
                

            
            

            resFile.close()
            stream.seek(0)
            stream.truncate()
           
