# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 pavle <pavle.portic@tilda.center>
#
# Distributed under terms of the MIT license.

import copy
import cv2 as cv
import numpy as np

def main():
	#  for i in [3, 7]:
	for i in range(1, 11):
		filename = 'set/A' + str(i) + '.png'
		src = cv.imread(filename)

		w, h, c = src.shape
		#  resize_coeff = 0.4
		#  src = cv.resize(src, (int(resize_coeff * h), int(resize_coeff * w)))
		box = find_resistor(src)

		if box is None:
			continue

		M = cv.moments(box)
		center = (int(M['m10']/M['m00']), int(M['m01']/M['m00']))
		box = sort_coords(box)

		x = abs(box[0][0] - box[2][0])
		y = abs(box[0][1] - box[2][1])
		phi = np.arctan2(y, x)

		if box[0][1] > box[2][1]:
			phi = -phi

		rotate_pt(box, center, -phi)
		box = sort_coords(box)

		rotM = cv.getRotationMatrix2D(center, np.degrees(phi), 1.0)
		src = cv.warpAffine(src, rotM, (h*2, w*2))

		box = np.int0(box)
		src = src[box[0][1]:box[1][1], box[0][0]:box[2][0]]

		if len(src) is 0:
			continue

		cv.imwrite(str(i) + '.png', src)


def rotate_pt(box, off, phi):
	sin = np.sin(phi)
	cos = np.cos(phi)
	for i in range(len(box)):
		pt = list(box[i])
		pt[0] -= off[0]
		pt[1] -= off[1]
		pt = [pt[0]*cos - pt[1]*sin, pt[1]*cos + pt[0]*sin]
		pt[0] += off[0]
		pt[1] += off[1]
		box[i] = pt


def sort_coords(box):
	for i in range(0, len(box)):
		for j in range(i + 1, len(box)):
			if box[j][0] < box [i][0] or (box[j][0] == box[i][0] and box[j][1] < box[i][1]):
				box[i], box[j] = list(box[j]), list(box[i])

	return box


def find_resistor(img):
	img = contrast(img, 1.6)
	img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	img = cv.medianBlur(img, 21)
	img = cv.Canny(img, 60, 100)
	kernel = np.ones((9, 9), np.uint8)
	img = cv.dilate(img, kernel, 2)
	img = cv.erode(img, kernel, 2)
	img, contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

	if len(contours) is not 0:
		max_index, max_area = max(enumerate([cv.contourArea(x) for x in contours]), key = lambda x: x[1])
		max_contour = contours[max_index]
		rect = cv.minAreaRect(max_contour)
		return cv.boxPoints(rect)

	return None


def contrast(img, clipLimit):
	img = cv.cvtColor(img, cv.COLOR_BGR2LAB)
	l, a, b = cv.split(img)
	clahe = cv.createCLAHE(clipLimit, tileGridSize=(8,8))
	cl = clahe.apply(l)
	img = cv.merge((cl, a, b))
	return cv.cvtColor(img, cv.COLOR_LAB2BGR)


if __name__ == "__main__":
	main()
