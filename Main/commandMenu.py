import chooseApp2
import tesseract
import GetImage
import cv2
import pyttsx
import camFind
import re

#This file allows the usage of different applications through voice commands.

#The voiceOverImage function uses the chooseApp2 file to select a function to activate
#To create a new function activated through voice simply add a pair to the dicionary appCommands bellow.
#e.g: 'info': infoCommand - when the user calls voiceOverImage and says 'info' into the mic the infoCommand
# 			  function is called. Where infoCommand is a function defined below in this file.

engine = pyttsx.init()
exitVar=False

#sends an image to the camfind application which returns a description of an object in the image
#leftSquare - a list of left hand coordinates used to crop the image: [left,top,height,width]
#leftSquare - a list of right hand coordinates used to crop the image: [left,top,height,width]
#img - a loaded image
def infoCommand(img, leftSquare,rightSquare):
	imgNew=GetImage.getImage(img, leftSquare,rightSquare)
	cv2.imwrite('./temp2.jpg',imgNew)
	infoVal=camFind.describeImage('./temp2.jpg')
	print infoVal
	say(infoVal)
	global exitVar
	exitVar=True

#sends an image to the OCR application which returns the text in the image.
#leftSquare - a list of left hand coordinates used to crop the image: [left,top,height,width]
#leftSquare - a list of right hand coordinates used to crop the image: [left,top,height,width]
#img - a loaded image	
def readCommand(img, leftSquare,rightSquare):
	imgNew=GetImage.getImage(img, leftSquare,rightSquare)
	cv2.imwrite('./temp1.jpg',imgNew)
	infoVal=tesseract.readImage('./temp1.jpg')
	print infoVal
	say(infoVal)
	global exitVar
	exitVar=True

#Preforms no action - Used when the image taken was not the one the 
#user wishes to preform an action on.
#parameters bellow may be None
#leftSquare - a list of left hand coordinates used to crop the image: [left,top,height,width]
#leftSquare - a list of right hand coordinates used to crop the image: [left,top,height,width]
#img - a loaded image	
def garbageCommand(img, leftSquare,rightSquare):
	global exitVar
	exitVar=True


def giveCommand():
	say('give command')
  

#A dictionary of the available commands, edit to delete/add commands.
#'command':functionName - where 'command' is the voice command used and function functionName is the name of the
#						  function which will be called upon the user saying 'command'  
appCommands={'info': infoCommand, 'read': readCommand,'exit': garbageCommand}


#activates a function which preforms an action on the image img according to the 
#user spoken command.
#leftSquare - a list of left hand coordinates used to crop the image: [left,top,height,width]
#leftSquare - a list of right hand coordinates used to crop the image: [left,top,height,width]
#img - a loaded image
def voiceOverImage(img, leftSquare,rightSquare):
        global exitVar
	#voice command until command understood.
	while (not(exitVar)):
                giveCommand()
		f=chooseApp2.voiceCommand(appCommands)
		f(img, leftSquare,rightSquare)
        exitVar=False
        
#uses text to speach to audibly read the string variable s.
def say(s):
	if (s==''):
		engine.say('error')
		engine.runAndWait()
		return
	s=re.sub('[^a-zA-Z    \n!"$%^&*()+_]','',s)
	engine.say(s)
	engine.runAndWait()		
