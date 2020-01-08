#from ObjectRecognizer import *
import pickle
import numpy as np
import cv2 as cv


def convert_to_absolute_coorditates(coord_list: list):
	absolute_coordinates_list = []
	with open('storage.pkl', 'rb') as f1:
		retval = pickle.load(f1)
		for pair in list(coord_list):
			pair = np.array([[pair]]).astype(np.float32)
			new_pair = cv.transform(pair, retval).tolist()[0][0]
			new_pair = [round(new_pair[0], 2), round(new_pair[1], 2)]
			absolute_coordinates_list.append(new_pair)
	return absolute_coordinates_list


def update_transormation_matrix():
	sr = np.array([
		[175, 417],
		[313, 171],
		[469, 331]
	])
	ds = np.array([
		[-40, -424],
		[30, -354],
		[-20, -290]
	])
	retval, inliers = cv.estimateAffine2D(sr, ds)
	with open('storage.pkl', 'wb') as f:
		pickle.dump(retval, f)
