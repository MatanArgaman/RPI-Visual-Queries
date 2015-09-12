import io
import picamera
import cv2
import cv
import time
import picamera.array
from HandDetection import handDetect
import HandDetection


	

hand_cascade = cv2.CascadeClassifier('cascadeMT.xml')
with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (160,120)
        while True:
            camera.capture(stream, format='bgr' , use_video_port = True)
            
            # At this point the image is available as stream.array
            image = stream.array
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.flip(gray,0)
            gray = cv2.flip(gray,1)
            handDetect(hand_cascade , gray ,detectLeft = True, getNegSamples = False)
            
            cv2.imshow('image',gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            stream.seek(0)
            stream.truncate()
        
          
        cv2.destroyAllWindows()
        
        
            
        

        



