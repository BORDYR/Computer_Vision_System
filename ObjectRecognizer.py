# For more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
import cv2 as cv2
import circlerecognizer
import AffineTransform

import cv2 as cv
import numpy as np
import os
import Rectanglerecognizer
import Rect_recoginzebycv
import time


def start_recognition(iterations = 0):
	cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
	img = cv2.imread('e1.png')
	if iterations:
		for _ in range(iterations):
			if (cap.isOpened()):
				# Capture frame-by-frame
				ret, frame = cap.read()
				ret = True
				frame = img
				#print('Got the frame')
				if ret == True:
					# frame = cv2.flip(frame,1)

					# Display the resulting frame
					circle_rating, outer = circlerecognizer.circle_recognise(frame) # распознавание кругов
					# outer = Rect_recoginzebycv.rec1(frame)			  # распознавание прямоуг от minAreaReact
					# outer = Rectanglerecognizer.get_image_with_realogram(frame)
					cv2.imshow('frame', outer)

				# time.sleep(0.5)
				else:
					break
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break
	else:
		while (cap.isOpened()):
			# Capture frame-by-frame
			ret, frame = cap.read()
			#print('Got the frame')
			if ret == True:
				t = time.time()
				frame = cv2.flip(frame, 1)

				# Display the resulting frame
				circle_rating, outer = circlerecognizer.circle_recognise(frame)  # распознавание кругов
				#outer = Rect_recoginzebycv.rec1(frame)			  # распознавание прямоуг от minAreaReact
				# outer = Rectanglerecognizer.get_image_with_realogram(frame)
				cv2.imshow('frame', outer)

			# time.sleep(0.5)
			else:
				break
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
	cap.release()
	return circle_rating


def get_defined_circles(circles_rating, n: int):
	defined_circles = []
	for k, v in circles_rating.items():
		if v > n/2:
			defined_circles.append(k.split(', ')[:2:])
	print(f'Finally there are {len(defined_circles)} objects:')
	print(defined_circles)
	return defined_circles

def get_objects_in_right_order(defined_circles: list):
	if len(defined_circles) == 1:
		return defined_circles
	else:
		for i in range(len(defined_circles)-1):
			if defined_circles[i][1] > defined_circles[i+1][1]:  # Changed < to >
				defined_circles[i], defined_circles[i+1] = defined_circles[i+1], defined_circles[i]
		return defined_circles


def send_coordinates_to_control_system(pipe_name='PipesOfPiece', data: str = 'test_message'):
	if not pipe_name:
		pipe_name = r'PipesOfPiece'
	pipe_path = r'\\.\pipe\PipesOfPiece' #TODO: can't concatenate '\\.\pipe\PipesOfPiece' and 'PipesOfPiece'
	message = data.encode('utf-8')
	with open(pipe_path, mode='r+b', buffering=0) as f:
		f.write(message)
		print('message sent')
		time.sleep(1)


def get_objects_coordinates():
	t = time.time()
	scan_frames_number: int = 50 # n is times of circle scan
	circles = start_recognition(scan_frames_number)
	def_circles = get_defined_circles(circles, scan_frames_number)
	ordered_circles = get_objects_in_right_order(def_circles)
	converted_circles = AffineTransform.convert_to_absolute_coorditates(ordered_circles)
	print(f'Recognition process took {round(time.time() - t, 2)} seconds')
	cv2.destroyAllWindows()
	return converted_circles

# When everything done, release the capture
