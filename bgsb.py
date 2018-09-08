from helperFiles import brightSet
import numpy as np
import cv2

path = 'input-video/0-0.mp4'
#path = 'input-video/0-1.mp4'


#path = 'input-video/1-0.mp4'

rad = 41
cntAreaMin = 30
#kernel = np.ones((3,3),np.uint8)

cap = cv2.VideoCapture(path)
fgbg = cv2.createBackgroundSubtractorMOG2()

xMin = float('inf')
yMin = float('inf')
xMax = float('-inf')
yMax = float('-inf')

i = 0
while True:
    ret, frame = cap.read()

    if frame is None:
	break

    fgmask = fgbg.apply(frame)
    #fgmask = cv2.erode(fgmask,kernel,iterations = 1)

    mask, contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
 
    if i%20 == 0:
	xMin = float('inf')
	yMin = float('inf')
	xMax = float('-inf')
	yMax = float('-inf')



    for cnt in contours:
	if cv2.contourArea(cnt) > cntAreaMin:
		X,Y,W,H = cv2.boundingRect(cnt)

		if X+W > xMax:
			xMax = X+W
		if Y+H > yMax:
			yMax = Y+H

		if X < xMin:
			xMin = X
		if Y < yMin:
			yMin = Y

		cv2.rectangle(frame,(X,Y),(X+W,Y+H),(0,255,0),2)


    if len(contours) > 0 and xMin < xMax:
    	cropFrame = frame.copy()[xMin:xMax,yMin:yMax]
    else:
	cropFrame = frame
    #cropFrame = frame.copy()[0:xMax,0:yMax]
   
    brightFrame = brightSet.findMaxBrightness(frame,cropFrame,(xMin,yMin),41)

    cv2.imshow('frame',frame)
    #cv2.imshow('frame crop',cropFrame)
    cv2.imshow('bg',fgmask)
    cv2.imshow('bright',brightFrame)

    i += 1

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
