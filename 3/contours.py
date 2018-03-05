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
	for k in range(1, 11):
		filename = 'set/A' + str(k) + '.png'
		src = cv.imread(filename)

		box = find_resistor(src)

		if box is None:
			continue

		src = crop_resistor(src, box)
		h, w, c = src.shape

		if len(src) is 0:
			continue

		img = np.zeros((1, w, 3), np.uint8)
		for i in range(w):
			sumB = 0
			sumR = 0
			sumG = 0
			for j in range(h):
				sumB += src[j, i, 0]
				sumR += src[j, i, 1]
				sumG += src[j, i, 2]

			img[0, i] = [ sumB/h, sumR/h, sumG/h ]

		kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
		img = cv.filter2D(img, -1, kernel)

		#  src = src.mean(3)
		#  print src[0]
		#  s = None
		#  cv.reduce(src, s, 0, cv.REDUCE_SUM, cv.CV_32S)

		#  cv.imshow('arst', img)
		cv.imwrite(str(k) + '.png', img)
		cv.waitKey()


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


def contrast(img, clipLimit):
	img = cv.cvtColor(img, cv.COLOR_BGR2LAB)
	l, a, b = cv.split(img)
	clahe = cv.createCLAHE(clipLimit, tileGridSize=(8,8))
	cl = clahe.apply(l)
	img = cv.merge((cl, a, b))
	return cv.cvtColor(img, cv.COLOR_LAB2BGR)


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


def crop_resistor(img, box):
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

	w, h, c = img.shape
	rotM = cv.getRotationMatrix2D(center, np.degrees(phi), 1.0)
	img = cv.warpAffine(img, rotM, (h*2, w*2))

	box = np.int0(box)
	x = box[0][0]
	y = box[0][1]
	w = box[2][0] - box[0][0]
	h = box[1][1] - box[0][1]
	y += int(0.2 * h)
	h = int(0.6 * h)
	img = img[y:(y+h), x:(x+w)]

	return img
	cv.imwrite(str(i) + '.png', img)


colors = {
	'black': {
		'iLowH': 0,
		'iHighH': 179,
		'iLowS': 0,
		'iHighS': 121,
		'iLowV': 0,
		'iHighV': 57,
	},
	'brown': {
		'iLowH': 7,
		'iHighH': 68,
		'iLowS': 0,
		'iHighS': 253,
		'iLowV': 0,
		'iHighV': 187,
	},
	'red': {
		'iLowH': 0,
		'iHighH': 4,
		'iLowS': 124,
		'iHighS': 255,
		'iLowV': 74,
		'iHighV': 255,
	},
	'orange': {
		'iLowH': 7,
		'iHighH': 85,
		'iLowS': 216,
		'iHighS': 255,
		'iLowV': 151,
		'iHighV': 255,
	},
	'yellow': {
		'iLowH': 10,
		'iHighH': 73,
		'iLowS': 250,
		'iHighS': 255,
		'iLowV': 225,
		'iHighV': 255,
	},
	'green': {
		'iLowH': 19,
		'iHighH': 165,
		'iLowS': 151,
		'iHighS': 255,
		'iLowV': 165,
		'iHighV': 194,
	},
	'blue': {
		'iLowH': 74,
		'iHighH': 149,
		'iLowS': 111,
		'iHighS': 255,
		'iLowV': 86,
		'iHighV': 255,
	},
	'purple': {
		'iLowH': 121,
		'iHighH': 150,
		'iLowS': 159,
		'iHighS': 194,
		'iLowV': 97,
		'iHighV': 164,
	},
	'gray': {
		'iLowH': 0,
		'iHighH': 80,
		'iLowS': 0,
		'iHighS': 80,
		'iLowV': 34,
		'iHighV': 139,
	},
	'white': {
		'iLowH': 0,
		'iHighH': 85,
		'iLowS': 0,
		'iHighS': 43,
		'iLowV': 144,
		'iHighV': 255,
	},
	'gold': {
		'iLowH': 18,
		'iHighH': 77,
		'iLowS': 93,
		'iHighS': 238,
		'iLowV': 81,
		'iHighV': 255,
	},
}


if __name__ == "__main__":
	main()
