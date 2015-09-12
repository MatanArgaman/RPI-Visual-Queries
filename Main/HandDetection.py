'''
Created on May 7, 2015

@author: ronen
'''
import cv2
import cv
import time
import numpy as np
import math
import picamera


def rotate_about_center(src, angle, scale=1.):
    w = src.shape[1]
    h = src.shape[0]
    rangle = np.deg2rad(angle)  # angle in radians
    # now calculate new image width and height
    nw = (abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale
    nh = (abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale
    # ask OpenCV for the rotation matrix
    rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
    # calculate the move from the old center to the new center combined
    # with the rotation
    rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5,0]))
    # the move only affects the translation, so update the translation
    # part of the transform
    rot_mat[0,2] += rot_move[0]
    rot_mat[1,2] += rot_move[1]
    return cv2.warpAffine(src, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv2.INTER_LINEAR)


def convertLH_RH(src):
    rotIm = rotate_about_center(src,90)
    rotIm = cv2.flip(rotIm,1)
    return rotIm

# converts a point (x,y) from a horizontally flipped and 90 ccw rotation back to original image coordinates    
def convertLHdet_to_imgCoords(lhand , origSize = (160,120) ):
    origW , origH = origSize
    currX , currY , currW , currH = lhand
    # Reverse the horizontal flip
    unFlipX = origH - currX;
    unFlipY = currY;
    #Reverse the rotation
    outX = origW - unFlipY;
    outY = unFlipX;
    return [outX-currW,outY-currH,currH,currW]

def validateLH_RelativeToRH(lh,rh):
    left_tlx , left_tly , lw , lheight = lh
    right_tlx , right_tly , rw , rheight = rh
    
    if left_tlx < right_tlx and  left_tly < right_tly :
        return True
    
    return False 
    
    
    

def handDetect(hand_cascade , img ,detectLeft = False, getNegSamples = False):
    rejectLevels =[]
    levelWeights = []

    

        
        
    start = time.time()

    if detectLeft:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = convertLH_RH(img)
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
#    faces = hand_cascade.detectMultiScale(gray, 1.1, 5,cv.CV_HAAR_FIND_BIGGEST_OBJECT,(30,30))
    #faces = hand_cascade.detectMultiScale(gray, 1.1,5)


    if not detectLeft:
        hands = hand_cascade.detectMultiScale(gray,rejectLevels,levelWeights, 1.1, 5,cv.CV_HAAR_FIND_BIGGEST_OBJECT,(50, 50),(260,260),True)
    else:
        hands = hand_cascade.detectMultiScale(gray,rejectLevels,levelWeights, 1.05, 5,cv.CV_HAAR_FIND_BIGGEST_OBJECT,(50, 50),(260,260),True)
        
    end = time.time()
    print "time elapsed for detection: ", end-start
    i = 0
    for (x,y,w,h) in hands:
        
        if detectLeft:
            #cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
            foundLHand = np.array([x,y,w,h])
            foundLHand = convertLHdet_to_imgCoords(foundLHand, origSize=(160,120))
            (nx,ny,nw,nh) = foundLHand
            cv2.rectangle(img,(nx,ny),(nx+nw,ny+nh),(0,255,0),2)
            hands[i] = foundLHand
        else:
            if not getNegSamples:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            
            else:
                cv2.imwrite('image'+str(x+y+w+h)+'.jpg',img)
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        i += 1
    
    
    return hands


def getFullResImage(camera , fullResStream , desiredRes):
    camera.resolution = desiredRes  
    #fullResStream = picamera.array.PiRGBArray(camera)                
    camera.capture(fullResStream, format='bgr' , use_video_port = True)
    fullResIm = fullResStream.array
    return fullResIm
