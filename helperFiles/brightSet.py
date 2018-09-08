import numpy as np
import cv2

prevLoc = None
prevRad = None

def insideExistingBox(newLoc,cntList,rad):
        y = newLoc[0]
	x = newLoc[1]
	w = 0
	h = 0

        for cntCmp in cntList:
                xCmp,yCmp,wCmp,hCmp = cv2.boundingRect(cntCmp)
                if x > xCmp and y > yCmp and x+w < xCmp+wCmp and y+h < yCmp+hCmp:
                        return True

        return False


def findMaxBrightness(frame,cropImage,minTup,cntList,rad):
	global prevLoc
	global prevRad

	xMin,yMin = minTup
	res = cropImage.copy()
	res1 = frame.copy()
	gray = cv2.cvtColor(cropImage, cv2.COLOR_BGR2GRAY)

	gray = cv2.GaussianBlur(gray, (rad, rad), 0)
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
	#image = orig.copy()
	#cv2.circle(res, maxLoc, rad, (255, 0, 0), 2)
	if not (xMin == float("inf") or yMin == float("inf")):
        	newLoc =  (int(maxLoc[0]+xMin),int(maxLoc[1]+yMin))
	else:
		newLoc = maxLoc

	'''
	if insideExistingBox(newLoc,cntList,rad):
		print 'inside'
		cv2.circle(res1, newLoc, rad, (0, 255, 0), 2)
		prevLoc = newLoc
		prevRad = rad
	elif prevLoc is not None and prevRad is not None:
		print 'lock on'
		cv2.circle(res1, prevLoc, prevRad, (0, 255, 0), 2)
	'''	
	cv2.circle(res1, newLoc, rad, (0, 255, 0), 2)
	prevLoc = newLoc
	prevRad = rad

	return res1
