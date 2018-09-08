from helperFiles import brightSet
import numpy as np
import cv2

#path = 'input-video/0-0.mp4'
path = 'input-video/0-1.mp4'

rad = 41

cap = cv2.VideoCapture(path)
fgbg = cv2.createBackgroundSubtractorMOG2()
while(1):
    ret, frame = cap.read()

    if ret is None:
	break

    fgmask = fgbg.apply(frame)

    brightFrame = brightSet.findMaxBrightness(frame,41)

    cv2.imshow('frame',frame)
    cv2.imshow('bg',fgmask)
    cv2.imshow('bright',brightFrame)


    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
