from helperFiles import brightSet
import numpy as np
import cv2
import os

path = 'input-video/4.mp4'
#path = 'input-video/2.mp4'
#path = 'input-video/1.mp4'
#path = 'input-video/0.mp4'
#path = 'input-video/0-0.mp4'
#path = 'input-video/0-1.mp4'
#path = 'input-video/1-0.mp4'
#path = 'input-video/2-0.mp4'

outPath = 'test.avi'


rad = 41
cntAreaMin = 30
#cntAreaMin = 20
#kernel = np.ones((3,3),np.uint8)

lockOnRefresh = 100


#timeRefresh = 2000
timeRefresh = 20

os.system('rm -rf datasetGen')
os.system('mkdir datasetGen')

def bgsb_info(): 
	cntList = []

	cap = cv2.VideoCapture(path)
	fgbg = cv2.createBackgroundSubtractorMOG2()

	fourcc = cv2.VideoWriter_fourcc(*'XVID')

	xMin = float('inf')
	yMin = float('inf')
	xMax = float('-inf')
	yMax = float('-inf')

	i = 0
	lockCnt = 0

	firstFrame = True

	while True:
	    cntList = []
	    ret, frame = cap.read()

	    if ret is None or frame is None:
		break
	    #print lockCnt
	    recFrame = frame.copy()

	    if firstFrame:
		out = cv2.VideoWriter(outPath, fourcc, 20.0, (frame.shape[1],frame.shape[0]))
		firstFrame = False
	    fgmask = fgbg.apply(frame)
	    #fgmask = cv2.morphologyEx(fgmask,cv2.MORPH_OPEN,kernel)

	    mask, contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	 
	    if i%timeRefresh == 0:
		#print 'Refresh'
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

			cv2.rectangle(recFrame,(X,Y),(X+W,Y+H),(255,0,0),2)
			cntList.append(cnt)

	    #print 'xMin: ', xMin, '   xMax: ', xMax
	    if len(contours) > 0 and xMin < xMax:
		cropFrame = frame.copy()[yMin:yMax,xMin:xMax]
		#cropFrame = frame.copy()
	    else:
		cropFrame = frame.copy()
	    #cropFrame = frame.copy()[0:xMax,0:yMax]
	   
	    brightFrame = brightSet.findMaxBrightness(frame,cropFrame,(xMin,yMin),cntList,(lockCnt,lockOnRefresh),41,True)

	    if cropFrame.shape[0] <= 0:
		continue

	    #cv2.imshow('frame',frame)
	    cv2.imshow('frame',recFrame)
	    cv2.imshow('frame crop',cropFrame)
	    cv2.imshow('bg',fgmask)
	    cv2.imshow('bright',brightFrame)

	    out.write(brightFrame)

	    i += 1
	    lockCnt += 1


	    k = cv2.waitKey(30) & 0xff
	    if k == 27:
		break
	cap.release()
	out.release()
	cv2.destroyAllWindows()



bgsb_info()
