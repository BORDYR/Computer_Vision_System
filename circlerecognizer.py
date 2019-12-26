import numpy as np
import collections
import operator
import argparse
import cv2
import time

image = cv2.imread('D:/PycharmProjects/object_detector_app/utils/j3.jpg')
circles_rating = collections.defaultdict(int)

def viewImage(image, window : str):
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    cv2.imshow(window, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def circle_recognise(image):
	output = image.copy()
	circles = get_circles(image)

	# ensure at least some circles were found
	if (circles is not None) :
		# convert the (x, y) coordinates and radius of the circles to integers
		circles = np.round(circles[0, :]).astype("int")
		# loop over the (x, y) coordinates and radius of the circles

		for (x, y, r) in circles:
			x, y, r = x.item(), y.item(), r.item()
			cv2.circle(output, (x, y), r, (0, 255, 0), 4)
			print(f'Circle has been detected! x = {x}p, y = {y}p, r = {r}p')
			cir = f'{x}, {y}, {r}'
			circles_rating[cir] += 1
	else:
		print('Circles haven\'t been found')
	return dict(circles_rating), output


def get_circles(image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# Detect circles in the image
	# Actual circle size is 25mm.
	#cv2.GaussianBlur(image, gray, ksize=)
	#gray = cv2.blur(gray, (2, 2))
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	circles = cv2.HoughCircles(image=gray, method=cv2.HOUGH_GRADIENT, dp=2, minDist=22, minRadius=25, maxRadius=32)

	height, width, channels = image.shape
	#print('height = {}, width = {}'.format(height, width))
	return circles
