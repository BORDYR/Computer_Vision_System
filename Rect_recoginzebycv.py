#!/usr/bin/env python

import sys
import numpy as np
import cv2 as cv

#check  cv.createBackgroundSubtractorMOG2()
#cv.BackgroundSubtractorKNN()


def rec1(frame):
	hsv_min = np.array((0, 54, 5), np.uint8)
	hsv_max = np.array((187, 255, 253), np.uint8)
	fn = 'image2.jpg'  # имя файла, который будем анализировать
	#img = cv.imread(fn)
	img = frame

	hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)  # меняем цветовую модель с BGR на HSV
	thresh = cv.inRange(hsv, hsv_min, hsv_max)  # применяем цветовой фильтр
	contours0, hierarchy = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

	# перебираем все найденные контуры в цикле
	for cnt in contours0:
		perimeter = cv.arcLength(cnt, True)
		if perimeter < 700:
			continue
		print(perimeter)
		rect = cv.minAreaRect(cnt)  # пытаемся вписать прямоугольник
		box = cv.boxPoints(rect)  # поиск четырех вершин прямоугольника
		box = np.int0(box)  # округление координат
		cv.drawContours(img, [box], 0, (255, 0, 0), 2)  # рисуем прямоугольник

	return img
	#cv.imshow('contours', img)  # вывод обработанного кадра в окно

	#cv.waitKey()
	#cv.destroyAllWindows()