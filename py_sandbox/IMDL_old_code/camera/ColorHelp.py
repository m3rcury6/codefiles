import sys
import cv2
import numpy as np

print "Enter in a BGR Value:"

#b=input('B: ')
#g=input('G: ')
#r=input('R: ')
(b,g,r)=input('BGR: ')
#print 'random: ',a,d,h
print 'BGR: ',b,g,r

bgr=np.uint8([[[b,g,r]]]) #list here
hsv=cv2.cvtColor(bgr,cv2.COLOR_BGR2HSV)
print "HSV: ", hsv

img=np.zeros((300,300,3),np.uint8)

#diagonal line, rectangle
#cv2.line(img,(0,0),(511,511),(255,0,0),5)
topLeft=(0,0)
botRight=(300,300)

cv2.rectangle(img,topLeft,botRight,(b,g,r),-10)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

print "done"


