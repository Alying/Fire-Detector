import numpy as np
import cv2

def findMaxBrightness(image, rad):
	res = image.copy()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	gray = cv2.GaussianBlur(gray, (rad, rad), 0)
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
	#image = orig.copy()
	cv2.circle(res, maxLoc, rad, (255, 0, 0), 2)

	return res
