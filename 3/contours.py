# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 pavle <pavle.portic@tilda.center>
#
# Distributed under terms of the MIT license.

import cv2 as cv
import numpy as np

def main():
	#  for i in [3, 7]:
	for i in range(1, 11):
		filename = 'set/A' + str(i) + '.png'
		src = cv.imread(filename)

		w, h, c = src.shape
		resize_coeff = 0.4
		src = cv.resize(src, (int(resize_coeff * h), int(resize_coeff * w)))
		box = find_resistor(src)
		cv.drawContours(src, [box], 0, (0, 255, 0), 1)
		cv.imshow('img', src)

		box = sorted(box, key=lambda coord: coord[0])

		x = abs(box[0][0] - box[2][0])
		y = abs(box[0][1] - box[2][1])
		phi = np.arctan2(y, x)

		print box

		if box[0][1] < box[2][1]:
			print 'right', np.degrees(phi)
		elif box[0][1] > box[2][1]:
			print 'left', np.degrees(phi)
		else:
			print 'hor', np.degrees(phi)

		cv.waitKey()


def find_resistor(img):
	img = contrast(img, 1.5)
	img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	img = cv.medianBlur(img, 7)
	img = cv.Canny(img, 100, 150)
	kernel = np.ones((9, 9), np.uint8)
	img = cv.dilate(img, kernel, 2)
	img = cv.erode(img, kernel, 2)
	img, contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

	if len(contours) is not 0:
		max_index, max_area = max(enumerate([cv.contourArea(x) for x in contours]), key = lambda x: x[1])
		max_contour = contours[max_index]
		rect = cv.minAreaRect(max_contour)
		return np.int0(cv.boxPoints(rect))


def contrast(img, clipLimit):
	img = cv.cvtColor(img, cv.COLOR_BGR2LAB)
	l, a, b = cv.split(img)
	clahe = cv.createCLAHE(clipLimit, tileGridSize=(8,8))
	cl = clahe.apply(l)
	img = cv.merge((cl, a, b))
	return cv.cvtColor(img, cv.COLOR_LAB2BGR)


if __name__ == "__main__":
	main()
