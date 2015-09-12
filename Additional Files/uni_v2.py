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


   

# def handDetect(img , getNegSamples = False):
#     rejectLevels =[]
#     levelWeights = []
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     start = time.time()
# #    faces = hand_cascade.detectMultiScale(gray, 1.1, 5,cv.CV_HAAR_FIND_BIGGEST_OBJECT,(30,30))
#     #faces = hand_cascade.detectMultiScale(gray, 1.1,5)
#     hands = hand_cascade.detectMultiScale(gray,rejectLevels,levelWeights, 1.1, 5,cv.CV_HAAR_FIND_BIGGEST_OBJECT,(50, 50),(260,260),True)
#     end = time.time()
#     print "time elapsed for detection: ", end-start
#     for (x,y,w,h) in hands:
#         if not getNegSamples:
#             cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
#             roi_gray = gray[y:y+h, x:x+w]
#             roi_color = img[y:y+h, x:x+w]
#         else:
#             cv2.imwrite('image'+str(x+y+w+h)+'.jpg',image)
#             cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
#     
#     
#     return hands




if __name__ == '__main__':
    pygame.mixer.init()
    global rbeep , lbeep
    rbeep= pygame.mixer.Sound('./beep_right.wav')
    lbeep= pygame.mixer.Sound('./beep_left.wav')
    
    hand_cascade = cv2.CascadeClassifier('cascadeMT.xml')

    RH_DET_THRESH = 3 # number of times it must be detected consecutively
    LH_DET_THRESH = 1 # number of times it must be detected consecutively    
    NUM_LEFT_ATTMEPTS = 3
    MAXDIST = 10
    RESIZE_FULL_RES_FACTOR = 5
    rhValidator = HandDetectValidator.HandDetectValidator(MAXDIST , RH_DET_THRESH)
    lhValidator = HandDetectValidator.HandDetectValidator(MAXDIST , LH_DET_THRESH)
    
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
                
                hands = handDetect(hand_cascade , image ,False,   False)
                rhValidator.feedNewHandList(hands)
                if rhValidator.checkForDetectionAndUpdateCounter():
                    rbeep.play()

                    
                    
                    #print rhValidator.foundHandPos
                    foundRHand = np.array(rhValidator.foundHandPos)
                    foundRHandFullSize = RESIZE_FULL_RES_FACTOR*foundRHand # 
                    print foundRHand
                    newx,newy,neww,newh = foundRHand
                    
                    # check for left in same frame and in num_attmept next frames
                    for i in range(NUM_LEFT_ATTMEPTS):
                        lhands = handDetect(hand_cascade, image, detectLeft = True, getNegSamples = False)
                        lhValidator.feedNewHandList(lhands)
                        if lhValidator.checkForDetectionAndUpdateCounter():
                            
                            foundLHand = np.array(lhValidator.foundHandPos)
                            foundLHand = HandDetection.convertLHdet_to_imgCoords(foundLHand, origSize=(160,120))
                            if HandDetection.validateLH_RelativeToRH(foundLHand, foundRHand):
                                lbeep.play()
                                fullResIm = HandDetection.getFullResImage(camera , fullResStream ,(160*RESIZE_FULL_RES_FACTOR , 120*RESIZE_FULL_RES_FACTOR))
                                foundLHandFullSize = RESIZE_FULL_RES_FACTOR*foundLHand
                                commandMenu.readCommand(fullResIm,foundLHandFullSize,foundRHandFullSize)
                                fullResStream.seek(0)
                                fullResStream.truncate()
                                camera.resolution = (160,120)
                    
                    
                        camera.capture(stream, format='bgr' , use_video_port = True)
                        image = stream.array
                        cv2.imshow('image',image)
                        
                        
                       
                
                cv2.imshow('image',image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                stream.seek(0)
                stream.truncate()
           
            cv2.destroyAllWindows()
