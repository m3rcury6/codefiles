import cv2
import numpy as np
import time
from common import clock, draw_str





#initialize threshold positions
ini=[0,108,110,179,255,255]
ini=[75,0,0,137,255,195] #0405: blue bin, kjg room
hL=ini[0]
sL=ini[1]
vL=ini[2]
hU=ini[3]
sU=ini[4]
vU=ini[5]


# return a processed frame from a given frame, no mouse stuff
def kjgProcess(inFrame): 
    # will included commented out code, to illustrate possibilities

        # flip frame about vertical axis
    # inFrame=cv2.flip(inFrame,1)

        # Resize the captured frame
    # ratio=0.5 #note, 1 = 1:1 ratio
    # inFrame = cv2.resize(inFrame,None,fx=ratio, fy=ratio, interpolation = cv2.INTER_AREA)

        # save semi-original for later
    inFrameOrig=inFrame

        # Gaussian Blur
    blurVal=5 #should be a positive odd number
    inFrame=cv2.GaussianBlur(inFrame,(blurVal,blurVal),0)
    FimgW=inFrame.shape[1]

    try:
        # color extract
        inFrame_hsv=cv2.cvtColor(inFrame,cv2.COLOR_BGR2HSV) #create HSV version #need fix here...
        bb,gg,rr=cv2.split(inFrame)
        lower=np.array([hL,sL,vL])
        upper=np.array([hU,sU,vU])
        inFrame=cv2.inRange(inFrame_hsv,lower,upper) #this is the true result
        inFrame_Gray=cv2.cvtColor(inFrame_hsv,cv2.COLOR_HSV2BGR) #back to BGR version
        inFrame_Gray=cv2.cvtColor(inFrame_Gray,cv2.COLOR_BGR2GRAY) #now to Grayscale

        #erode then dilate, aka open the image
        morphVal=11 #should be a positive odd number
        kernel = np.ones((morphVal,morphVal),np.uint8)
        inFrame = cv2.morphologyEx(inFrame, cv2.MORPH_OPEN, kernel) 

        # combine and threshold 
        inFrame=cv2.bitwise_and(inFrame_Gray,inFrame_Gray,mask=inFrame)

        # now make everything not-black into white. 
        ret,inFrame2=cv2.threshold(inFrame,0,255,cv2.THRESH_BINARY)

        # find contours
        FFcontours, hierarchy = cv2.findContours(inFrame2,\
            cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        # REMEMBER TO HIDE ME xx
        # superimpose contours onto a frame
        cv2.drawContours(inFrameOrig, FFcontours, -1, (0,255,0), 1) 

        # find moments, get centroid (as long as there are contours)
        if len(FFcontours) > 0: 

            # first, want to find the largest contour, by area: 
            try:
                Floc=FFcontours.index(max(FFcontours,key=cv2.contourArea))
            # print loc
            except ValueError:
                print "ValueError: loc set to 0"
                Floc=0

            # ensure never go out of bounds
            if(Floc>len(FFcontours)):
                print "OutOfBoundsError: loc set to zero"
                Floc=0

            Fcnt=FFcontours[Floc]
            
            # create bounding circle
            (Fxcirc,Fycirc),Frcirc=cv2.minEnclosingCircle(Fcnt)

            # center = (int(Fxcirc),int(Fycirc))
            # cv2.circle(frameOrig,center,int(rcirc),(255,0,0),2)
            # cv2.line(frameOrig,(0,0),(300,300),(255,255,255),4)
            # print type(inFrameOrig)

            return (Fxcirc,Fycirc,Frcirc,FimgW,inFrameOrig)
            # return (Fxcirc,Fycirc,Frcirc)

    except:
        print "ColorspaceError"
        # print type(inFrameOrig)
        return (0,0,0,100,inFrame)

# make for angle correction: 
def angleError(raw_cx,FrameWidth):
    cc=float(raw_cx)
    va=float(75) #degrees
    fw=float(FrameWidth)
    return va/fw*(cc-fw)+va/2

# draw results
def kjgDraw(xx,yy,rr,ff):
    # circle of identified object
    cv2.circle(ff,(int(xx),int(yy)),int(rr),(0,0,255),2)

    #create crosshairs (optional)
    imgH=ff.shape[0]
    imgW=ff.shape[1]
    cv2.line(ff,(imgW/2,0),(imgW/2,imgH),(0,0,0),1)
    cv2.line(ff,(0,imgH/2),(imgW,imgH/2),(0,0,0),1)
	# delme
    #create 2D error line
    cv2.line(ff,(imgW/2,imgH/2),(int(xx),int(yy)),(255,0,255),1)
    
    # print current threshold range
    str1=str(hL)+','+str(sL)+','+str(vL)
    str2=str(hU)+','+str(sU)+','+str(vU)
    draw_str(ff,(60,20),str1)
    draw_str(ff,(60,50),str2)



# setup mouse color selection: 
drawing = False # true if mouse is pressed
ix,iy = -1,-1
counter=0
createWin=False
# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,moving,createWin
    circleRadius=10
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        moving = True
        ix,iy=x,y


    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        moving = False
        createWin=True

cv2.namedWindow('contours')
cv2.setMouseCallback('contours',draw_circle)

box=21 # Mouse Selection Box, probably ideally odd/positive
ROIb=0 #initialize ROI colors
ROIg=0
ROIr=0
# end of mouse color selection setup

aa=int(raw_input("select video source: "))
cap = cv2.VideoCapture(aa) #select video source

t=time.time() #used to get looptime


while(1):
    # Take each frame
    _, frame = cap.read()

    try:
        xx,yy,rr,imgW,ff=kjgProcess(frame)
        # xx,yy,rr,imgW=kjgProcess(frame)
    except TypeError:
        xx=0; yy=0; rr=0; imgW=100;ff=frame
        # print "TypeError: rr = ",rr
        # NOTE: this error happens when no objects are detected.
        # during media day, this is unlikely, noise is sure to 
        # be detected

    # if successful, draw it all
    if(rr !=0):
        kjgDraw(xx,yy,rr,ff)
        #return degrees off from center, from pixels.
        asdf=int(angleError(xx,imgW))
    else:
        asdf='!'

    print asdf
# DO NOT DELETE THIS, MOUSE CLICKING CAN STILL BE USEFUL
    # # if mouse is being used, show the selection box
    # if(drawing==True and moving==True):
    #     # print "drawing"
    #     # cv2.circle(img,(ix,iy),10,(0,0,255),2)
    #     cv2.rectangle(ff,(ix-(box-1)/2,iy-(box-1)/2),\
    #         (ix+(box-1)/2,iy+(box-1)/2),(0,0,255),2)
    # # when done clicking, show averaged color
    # cv2.rectangle(ff,(1,1),(50,50),(ROIb,ROIg,ROIr),-1)
    # #when mouse is unclicked (lifted), create ROI image
    # if(createWin==True):    
    #     xMin=ix-(box-1)/2
    #     xMax=ix+(box-1)/2
    #     yMin=iy-(box-1)/2
    #     yMax=iy+(box-1)/2
    #     roi=ff[yMin:yMax,xMin:xMax]
    #     # roi=cv2.GaussianBlur(roi,(5,5),0)
    #     roi=cv2.blur(roi,(15,15))
    #     ROIb,ROIg,ROIr,_ = cv2.mean(roi)
    #     # print ROIb,ROIg,ROIr
    #     # cv2.imshow('roi',roi)
    #     createWin=False
    #     # get bgr and convert it to hsv values
    #     ROIbgr = np.uint8([[[ROIb,ROIg,ROIr]]])
    #     ROIhsv = cv2.cvtColor(ROIbgr,cv2.COLOR_BGR2HSV)
    #     ROIh=int(ROIhsv[0][0][0])
    #     ROIs=int(ROIhsv[0][0][1])
    #     ROIv=int(ROIhsv[0][0][2])
    #     # take hsv values, make lower/upper ranges
    #     hff=20 # h offset
    #     sff=80 #s offset
    #     vff=40 #v offset
    #     hL=max(ROIh-hff,0) #min/abs to prevent out of range error
    #     sL=max(ROIs-sff,0)
    #     vL=max(ROIv-vff,0)
    #     hU=min(ROIh+hff,179)
    #     sU=min(ROIs+sff,255)
    #     vU=min(ROIv+vff,255)
    #     # need to deal with red color somehow: 
    #     if(hL < 10 or hU > 245): 
    #         hL=0
    #         hU=255

    try:
        cv2.imshow('contours',ff)
    except:
        print "VideoFrameError"

    # # get loop time (KJGNOTE: typ loop time below 45ms on laptop)
    # print int((time.time()-t)*1000)
    # t=time.time()

    #end program when hit 'Escape' key
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()



    # COPY-ABLE CODE TO GO FROM HSV TO GRAYSCALE, DO NOT REMOVE
    # #get from HSV to Grayscale
    # lala=cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR) #back to BGR version
    # lala=cv2.cvtColor(lala,cv2.COLOR_BGR2GRAY) #now to Grayscale
    # cv2.imshow('to grayscale',lala)
