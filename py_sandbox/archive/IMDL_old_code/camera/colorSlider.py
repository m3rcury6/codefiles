import cv2
import numpy as np

def nothing(x):
    pass

# Create a black image, a window
height=200
width=512
img = np.zeros((height,width,3), np.uint8)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)

cv2.createTrackbar('H','image',0,179,nothing)
cv2.createTrackbar('S','image',0,255,nothing)
cv2.createTrackbar('V','image',0,255,nothing)

cv2.createTrackbar('H3','image',0,179,nothing)
cv2.createTrackbar('S3','image',0,255,nothing)
cv2.createTrackbar('V3','image',0,255,nothing)


#here, (x,y)
tL=(10,30)
bR=(width/3-10,height*7/8)

tL2=(width/3+10,30)
bR2=(width*2/3-10,height*7/8)

tL3=(width*2/3+10,30)
bR3=(width-10,height*7/8)

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of multiple trackbars
    #trackbar set 1 - BGR
    r = cv2.getTrackbarPos('R','image')
    g = cv2.getTrackbarPos('G','image')
    b = cv2.getTrackbarPos('B','image')
    #track set 2 - HSV
    h = cv2.getTrackbarPos('H','image')
    s = cv2.getTrackbarPos('S','image')
    v = cv2.getTrackbarPos('V','image')    
    hsv=np.uint8([[[h,s,v]]])   #must also transform to BGR
    bgr2=cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
    b2=int(bgr2[0][0][0])
    g2=int(bgr2[0][0][1])
    r2=int(bgr2[0][0][2])
    #trackset 3 - HSV3
    h3 = cv2.getTrackbarPos('H3','image')
    s3 = cv2.getTrackbarPos('S3','image')
    v3 = cv2.getTrackbarPos('V3','image')
    hsv3=np.uint8([[[h3,s3,v3]]])    #must also transform to BGR
    bgr3=cv2.cvtColor(hsv3,cv2.COLOR_HSV2BGR)
    b3=int(bgr3[0][0][0])
    g3=int(bgr3[0][0][1])
    r3=int(bgr3[0][0][2])


    #plot everything
    img[:] = 0  #set background to black
    cv2.rectangle(img,tL,bR,(b,g,r),-1) #plot rect1
    cv2.rectangle(img,tL2,bR2,(b2,g2,r2),-1)    #plot rect2
    cv2.rectangle(img,tL3,bR3,(b3,g3,r3),-1)    #plot rect3
    #"plot in img, dims tL to bR, color (bgr), thickness -1"

cv2.destroyAllWindows()

