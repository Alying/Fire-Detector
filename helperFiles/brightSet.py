import numpy as np
import cv2

def findMaxBrightness(frame,image,minTup,rad):
	xMin,yMin = minTup
	res = image.copy()
	res1 = frame.copy()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	gray = cv2.GaussianBlur(gray, (rad, rad), 0)
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
	#image = orig.copy()
	#cv2.circle(res, maxLoc, rad, (255, 0, 0), 2)
	if not (xMin == float("inf") or yMin == float("inf")):
        	newLoc =  (int(maxLoc[0]+yMin),int(maxLoc[1]+xMin))
	else:
		newLoc = maxLoc


	min_thresh = (min_val+1e-6)*1.5
	match_locations = np.where()

	cv2.circle(res1, newLoc, rad, (0, 255, 0), 2)

	return res1
