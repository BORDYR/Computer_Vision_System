import numpy as np
import argparse
import cv2

image = cv2.imread('D:/PycharmProjects/object_detector_app/utils/j3.jpg')

def viewImage(image, window : str):
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    cv2.imshow(window, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def circle_recognise(image):

	#viewImage(image)
	# load the image, clone it for output, and then convert it to grayscale
	#image = cv2.imread(args["image"])
	output = image.copy()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# detect circles in the image
	circles = cv2.HoughCircles(image=gray, method=cv2.HOUGH_GRADIENT, dp=2, minDist=2000, minRadius=50, maxRadius=200)
	height, width, channels = image.shape
	print('height = {}, width = {}'.format(height, width))
	# ensure at least some circles were found
	if circles is not None:
		# convert the (x, y) coordinates and radius of the circles to integers
		circles = np.round(circles[0, :]).astype("int")

		# loop over the (x, y) coordinates and radius of the circles
		for (x, y, r) in circles:
			cv2.circle(output, (x, y), r, (0,255,0), 4)
			print('Circle has been detected! x = {}p, y = {}p, r = {}p'.format(x, y, r))
			#viewImage(output, 'frame')
			#cv2.imshow('ff', output)
	else:
		print('Circles haven\'t been found')
	return output
#circle_recognise(image)
		# show the output image

		#cv2.imshow("output", np.hstack([image, output]))
		#cv2.waitKey(0)
