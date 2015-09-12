import commandMenu
import cv2

image=cv2.imread('/home/pi/Desktop/Apps/OCR_App/b.jpg')
commandMenu.readCommand(image,[0,0,0,0],[87,300,100,100])
