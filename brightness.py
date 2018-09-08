# USAGE
# python bright.py --image images/retina.png --radius 41
# python bright.py --image images/retina-noise.png --radius 41
# python bright.py --image images/moon.png --radius 61

# import the necessary packages
import numpy as np
import cv2

rad = 41
path = 'input-video/0-0.mp4'

cap = cv2.VideoCapture(path)

while True:
	# load the image and convert it to grayscale
	ret, image = cap.read()

	if ret is None or image is None:
		break
	orig = image.copy()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# perform a naive attempt to find the (x, y) coordinates of
	# the area of the image with the largest intensity value
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
	cv2.circle(image, maxLoc, 5, (255, 0, 0), 2)

	# display the results of the naive attempt
	cv2.imshow("Naive", image)

	# apply a Gaussian blur to the image then find the brightest
	# region
	gray = cv2.GaussianBlur(gray, (rad, rad), 0)
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
	image = orig.copy()
	cv2.circle(image, maxLoc, rad, (255, 0, 0), 2)

	# display the results of our newly improved method
	cv2.imshow("Robust", image)
	cv2.waitKey(1)
