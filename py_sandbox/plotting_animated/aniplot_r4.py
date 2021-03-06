'''
datecreated: 190930
objective: want to use opencv to make some kind of animated plotting tool.
note: using cv2 is MUCH MUCH faster, will use this instead of matplotlib
applications:
    * animated plot
    * live updating
    * user / computer controlled animation

alright, idea:
1. have a object move around in a circle constantly, perpetually
2. show item, updating position
3. also be able to plot static items like walls, etc


steps:
1. have a window with shapes
2. have those shapes move around
3. have those shapes move with tkinter control
4. have those shapes move with computer control

THINGS TO IMPLEMENT
status | want
done   | plot fast-updating (60Hz+) plot area
done   | have a rotating rectangle
done   | use polygons instead of "rect", in custom function
???    | overlay simple image on top of background (deal with alpha)
???    | have item follow a path
???    | be able to control item with keyboard
???    |


'''

# import matplotlib.pyplot as plt
# import matplotlib.animation as ani
import cv2
import time
import numpy as np
RED = (0,0,255) # for use with opencv (BGR)
BLU = (255,0,0)
GRN = (0,255,0)
WHT = (255,255,255)
BLK = (0,0,0)
CVFONT = cv2.FONT_HERSHEY_SIMPLEX
IMW=400
IMH=300
def qs(img,title='CLOSE WITH KEYBOARD'):
    cv2.imshow(title,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def rect2(img, center,dims,angle, color,*kargs):
    ''' general steps:
    1. take in parameters
    2. rotate rectangle centered at origin
    3. translate to given spot.

     '''
    xc,yc=center
    w,h=dims
    theta = np.radians(angle)
    c,s=np.cos(theta),np.sin(theta)
    R=np.array([
        [c,-s,0],
        [s,c,0],
        [0,0,1]]) # 3x3
    pts=np.array([
        [-w,h,1],
        [w,h,1],
        [w,-h,1],
        [-w,-h,1],
        [-w,h,1]   ])/2

    # rotate points
    pts2=pts@R
    pts2[:,0]+=xc
    pts2[:,1]+=yc
    pts2=pts2[:,:2].reshape((-1,1,2)).astype(int)
    cv2.polylines(img,[pts2],True,RED)

t0=time.time()

class Timer:
    def __init__(self):
        self.t0=time.time() # start time
    def now(self):
        ''' return time since start of program '''
        return time.time()-self.t0
timer = Timer()
NOW=timer.now

xc=IMW/2
yc=IMH/2
w=50
h=100

while(True):
    t1=time.time()-t0
    t0=time.time()
    bkgd = np.ones((IMH,IMW,3))*255 # follows image format
    cv2.putText(bkgd,str(round(t1,3)),(50,30),CVFONT,1,BLU)
    cv2.putText(bkgd,str(round(NOW(),3)),(50,60),CVFONT,1,BLU)
    cv2.circle(bkgd,(int(IMW/2),int(IMH/2)),10,GRN)
    rect2(bkgd,(xc,yc),(w,h),NOW()*180,RED)
    pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
    pts = pts.reshape((-1,1,2)) # critical for drawing a polygon

    cv2.imshow('frame',bkgd)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
