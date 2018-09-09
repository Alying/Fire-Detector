import numpy as np
import cv2
import twilio_sms

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)
    
import sys
sys.stdout = Unbuffered(sys.stdout)


prevLoc = None
prevRad = None

prevFlameSize = 0
sizeUpdateInterval = 5000

abnormalConst = 4.0

picSaveCount = 0

abNormInital = True

alreadySentText = False

def abnormalRateChange(count,currSize):
    global abNormInital
    global prevFlameSize
    # Compares size from past to the current value

    if abNormInital:
        # To initalize the prevFlameSize value
        prevFlameSize = currSize
        abNormInital = False
        return False

    if currSize == 0:
        currSize = 0.000001

    # Abnormal decrease (probably found actual fire)
    if float(prevFlameSize)/float(currSize) > 6.0:
        print ('Adjusting referernce size')
        prevFlameSize = currSize
        return False

    if float(currSize)/float(prevFlameSize) > abnormalConst:
        # Fire growth is abnormal, danger of wild fire is alerted
        print ('currSize: ', currSize, '  prevFlameSize: ', prevFlameSize)
        return True

    if count%sizeUpdateInterval == 0:
        print ('Updating flame')
        prevFlameSize = currSize

    return False

def analyzeSize(frame):
	gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(gray_frame,127,255,cv2.THRESH_BINARY)
	_,contours,hierarchy = cv2.findContours(thresh, 1, 2)

	maxSize = float('-inf')
	for cnt in contours:
		if cv2.contourArea(cnt) > maxSize:
			maxSize = cv2.contourArea(cnt)

	cv2.imshow('thresh',thresh)

	return maxSize

def insideExistingBox(newLoc,cntList,rad):
    x = newLoc[0]
    y = newLoc[1]
    w = 0
    h = 0

    for cntCmp in cntList:
            xCmp,yCmp,wCmp,hCmp = cv2.boundingRect(cntCmp)
            if x > xCmp and y > yCmp and x+w < xCmp+wCmp and y+h < yCmp+hCmp:
                    return True

    return False


def findMaxBrightness(frame,cropImage,minTup,cntList,lockOnTup,rad,picOn):
    global prevLoc
    global prevRad
    global picSaveCount
    global alreadySentText

    lockCnt, lockOnRefresh= lockOnTup
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

    if lockCnt == 0 or ((lockCnt%lockOnRefresh == 0) and insideExistingBox(newLoc,cntList,rad)):
        # This is for initalization or if we want to refresh
        print ('Relocalizing')
        #cv2.circle(res1, newLoc, rad, (0, 255, 0), 2)

        if rad > newLoc[1] or rad > newLoc[0] :
            rad = min(newLoc[1],newLoc[0])

        
        cropFrame = res1.copy()[newLoc[1]-rad:newLoc[1]+rad, newLoc[0]-rad:newLoc[0]+rad]
        cv2.rectangle(res1,(newLoc[0]-rad,newLoc[1]-rad),(newLoc[0]+rad,newLoc[1]+rad),(0,255,0),2)
        prevLoc = newLoc
        prevRad = rad
    else:

        if rad > prevLoc[1] or rad > prevLoc[0]:
            rad = min(prevLoc[1],prevLoc[0])

        cropFrame = res1.copy()[prevLoc[1]-rad:prevLoc[1]+rad, prevLoc[0]-rad:prevLoc[0]+rad]
        #cv2.circle(res1, prevLoc, prevRad, (0, 255, 0), 2)
        cv2.rectangle(res1,(prevLoc[0]-rad,prevLoc[1]-rad),(prevLoc[0]+rad,prevLoc[1]+rad),(0,255,0),2)

    if picOn:
        saveStr = './datasetGen/' + str(picSaveCount)+'.png'
        cv2.imwrite(saveStr, cropFrame)
        picSaveCount += 1

    flameArea = analyzeSize(cropFrame)
    textWrite = 'Fire size: '+str(flameArea)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(res1,textWrite,(10,40),font,1,(255,255,255),1,cv2.LINE_AA)


    # Check to see if the fire in danger of becoming wild fire
    if abnormalRateChange(lockCnt,flameArea) and not alreadySentText:
        print ('WARNING: CURRENT FIRE IS AT RISK OF BECOMING A WILD FIRE!')
        twilio_sms.send_text('WARNING: CURRENT FIRE IS AT RISK OF BECOMING A WILD FIRE!')
        alreadySentText = True

    return res1
