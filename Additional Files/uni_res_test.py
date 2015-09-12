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
    
    
    with picamera.PiCamera() as camera:
        fullResStream = picamera.array.PiRGBArray(camera)
        with picamera.array.PiRGBArray(camera) as stream:
            camera.resolution = (1280,960)
            #i = 0
            fr = 1
            adetectRight = False
            while True:
                camera.capture(stream, format='bgr' , use_video_port = True)
                
                # At this point the image is available as stream.array
                image = stream.array
                
                if adetectRight:
                    hands = handDetect(hand_cascade , image ,detectLeft = False,  getNegSamples = False)
                    rhValidator.feedNewHandList(hands)
                    if rhValidator.checkForDetectionAndUpdateCounter():
                        rbeep.play()
                        #print rhValidator.foundHandPos
                        foundRHand = np.array(rhValidator.foundHandPos)
                        foundRHandFullSize = RESIZE_FULL_RES_FACTOR*foundRHand # 
                        print foundRHand
                        newx,newy,neww,newh = foundRHand
                        detectRight = False
                
                        
                        numLeftAttempts += 1
                        if numLeftAttempts == MAX_NUM_LEFT_ATTMEPTS:
                            numLeftAttempts = 0 # reset
                            detectRight = True
                        
                        
                       
                
                cv2.imshow('image',image)
                print '\n'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                stream.seek(0)
                stream.truncate()
           
            cv2.destroyAllWindows()
