'''
Created on Apr 28, 2015

@author: ronen
'''

import numpy as np
import math


class HandDetectValidator:
    def __init__(self , maxDist , thresh):
        self.count = 0    
        self.THRESH = thresh
        self.maxDist = maxDist
        self.currHands = []
        self.handFound = False
        self.foundHandPos = []
     
    def reset(self):
         self.count = 0
         self.currHands = []
         self.handFound = False
         self.foundHandPos = []
    
    def checkForMatches(self , hands):
        i = 0
        k = 0
        toSave = []
        updatedHands = []
        for (xNew,yNew,wNew,hNew) in hands:
            for (x,y,w,h) in self.currHands:
                dist = math.sqrt(np.linalg.norm(np.array([xNew-x , yNew -y]), 2))
                if dist <= self.THRESH:
                    toSave.append(i)
                    if toSave.count(i) == 1:
                        updatedHands.append([ xNew,yNew,wNew,hNew])
                i += 1
            
            
            k +=1
        
        self.currHands = updatedHands
        
        
    def feedNewHandList(self, hands):
        if len(hands) == 0:
            return;

        if self.count == 0:
            self.currHands = hands
            self.count += 1
        else:
            self.checkForMatches(hands)
            if len( self.currHands) > 0:
               self.count += 1
               
            else: # no hands found that match previous hands
                self.reset()
        if self.count >= self.THRESH:
            self.handFound = True
            self.foundHandPos = self.currHands[0] # TODO should decide what to do in case of multiple hands
            print "Found hand!\n"
                
                
                
    def checkForDetectionAndUpdateCounter(self):
        if self.count >= self.THRESH:
            self.count = 0
            return True
        else:
            return False
