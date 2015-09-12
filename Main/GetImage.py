
import cv2;
from cv2 import waitKey
import copy

#constants

upperLeftXpercentage=0.4;
upperLeftYpercentage=0.5;
bottomRightXpercentage=0.3;
bottomRightYpercentage=0.5;
bottomLeftXpercentage=1.0-bottomRightXpercentage;
bottomLeftYpercentage=bottomRightYpercentage;
upperRightXpercentage=1.0-upperLeftXpercentage;
upperRightYpercentage=upperLeftYpercentage;


#img - is a loaded image
#b1 - a list of left hand coordinates used to crop the image: [left,top,height,width]
#b1 - a list of right hand coordinates used to crop the image: [left,top,height,width]
#return - A cropped image of a square between the hands.
def getImage(img, b1,b2):
    c1=copy.copy(b1)
    c2=copy.copy(b2)
    #where c1=[xmin,ymin,xmax,ymax] is the coordinates of the first corner
	#where c1=[xmin,ymin,xmax,ymax] is the coordinates of the second corner
    c1[2]=c1[0]+c1[2]
    c1[3]=c1[1]+c1[3]
    c2[2]=c2[0]+c2[2]
    c2[3]=c2[1]+c2[3]
    print 'c2: ' , c2
        
    if (c1[0]>c1[0]): #swap
        c3=c1;
        c1=c2;
        c2=c3;
        
    if (c1[1]<c2[1]):
        #c1 is an upper left corner (assume then that c2 is a bottom right corner).
        minX=c1[0]+int((float(c1[2]-c1[0]))*upperLeftXpercentage);
        minY=c1[1]+int((float(c1[3]-c1[1]))*upperLeftYpercentage);
        maxX=c2[0]+int((float(c2[2]-c2[0]))*bottomRightXpercentage);
        maxY=c2[1]+int((float(c2[3]-c2[1]))*bottomRightYpercentage);
    else:
        #c1 is an bottom left corner (assume then that c2 is an upper right corner).
        minX=c1[0]+int((float(c1[2]-c1[0]))*bottomLeftXpercentage);
        maxY=c1[1]+int((float(c1[3]-c1[1]))*bottomLeftYpercentage);
        minY=c2[1]+int((float(c2[3]-c2[1]))*upperRightXpercentage);
        maxX=c2[0]+int((float(c2[2]-c2[0]))*upperRightYpercentage);
    cv2.imwrite('./img.jpg',cutImage(img,[minX,minY,maxX,maxY]))  
    print 'actual cutting point: ', [minX,minY,maxX,maxY]  
    return cutImage(img,[minX,minY,maxX,maxY]);
    

#img - is an image
#where c1=[xmin,ymin,xmax,ymax] is the square of the cut image
def cutImage(img, c): 
    return img[c[1]:c[3],c[0]:c[2]]


#usage example:
    
# img=cv2.imread('D:\\bin\\images\\IMG_6207.jpg');
# imgNew=getImage(img, [50,50,100,100],[400,300,450,350])
# #imgNew=cutImage(img,[100, 400, 100, 350]);
# 
# cv2.imshow("bah",imgNew)
# waitKey(0)


