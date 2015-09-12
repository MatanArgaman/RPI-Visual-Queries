import commandMenu
import io
import picamera
import cv2
import cv
import time
import HandDetectValidator
import picamera.array
import numpy as np
import pygame


   

def handDetect(img , getNegSamples = False):
    rejectLevels =[]
    levelWeights = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    start = time.time()
#    faces = hand_cascade.detectMultiScale(gray, 1.1, 5,cv.CV_HAAR_FIND_BIGGEST_OBJECT,(30,30))
    #faces = hand_cascade.detectMultiScale(gray, 1.1,5)
    hands = hand_cascade.detectMultiScale(gray,rejectLevels,levelWeights, 1.1, 5,cv.CV_HAAR_FIND_BIGGEST_OBJECT,(50, 50),(260,260),True)
    end = time.time()
    print "time elapsed for detection: ", end-start
    for (x,y,w,h) in hands:
        if not getNegSamples:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
        else:
            cv2.imwrite('image'+str(x+y+w+h)+'.jpg',image)
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    
    
    return hands




if __name__ == '__main__':
    pygame.mixer.init()
    global beep
    beep= pygame.mixer.Sound('./beep_ping.wav')
    
    hand_cascade = cv2.CascadeClassifier('cascadeMT.xml')

    RH_DET_THRESH = 3 # number of times it must be detected consecutively
    MAXDIST = 10
    rhValidator = HandDetectValidator.HandDetectValidator(MAXDIST , RH_DET_THRESH)
    
    with picamera.PiCamera() as camera:
        fullResStream = picamera.array.PiRGBArray(camera)
        with picamera.array.PiRGBArray(camera) as stream:
            camera.resolution = (160,120)
            #i = 0
            fr = 1
            while True:
                camera.capture(stream, format='bgr' , use_video_port = True)
                
                # At this point the image is available as stream.array
                image = stream.array
                
                hands = handDetect(image , False)
                rhValidator.feedNewHandList(hands)
                if rhValidator.checkForDetectionAndUpdateCounter():
                    beep.play()

                    camera.resolution = (800,600)
                    camera.capture(fullResStream, format='bgr' , use_video_port = True)
                    fullresIm = fullResStream.array
                    #print rhValidator.foundHandPos
                    foundRHand = np.array(rhValidator.foundHandPos)
                    foundRHand = 5*foundRHand
                    print foundRHand
                    leftHand = [0,0,0,0]
                    
                    
                    commandMenu.readCommand(fullresIm,leftHand,foundRHand)
                    newx,newy,neww,newh = foundRHand
                    cv2.rectangle(fullresIm,(newx,newy),(newx+neww,newy+newh),(255,0,0),2)
                    cv2.imwrite('./Origimg.jpg',fullresIm)
                    fullResStream.seek(0)
                    fullResStream.truncate()
                    camera.resolution = (160,120)
                    
                       
                
                cv2.imshow('image',image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                stream.seek(0)
                stream.truncate()
           
            cv2.destroyAllWindows()
