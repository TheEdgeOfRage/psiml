# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 pavle <pavle.portic@tilda.center>
#
# Distributed under terms of the MIT license.


#  cpy = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
#  cv.drawContours(cpy, [np.int0(rect)], 0, (0, 0, 255), 2)
#  cv.imshow('arst', cpy)
#  cv.waitKey()

import copy
import cv2 as cv
import numpy as np

def main():
	for k in range(1, 11):
	#  for k in [5]:
		filename = 'set/A' + str(k) + '.png'
		src = cv.imread(filename)

		box = find_resistor(src)

		if box is None:
			continue

		src = crop_resistor(src, box)

		if len(src) is 0:
			continue

		simple = simplify_image(src)
		find_bands(simple)

		#  src = src.mean(3)
		#  print src[0]
		#  s = None
		#  cv.reduce(src, s, 0, cv.REDUCE_SUM, cv.CV_32S)

		cv.imshow(str(k), simple)
		cv.waitKey()
		#  cv.imwrite(str(k) + '.png', simple)


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
	rect = None

	if len(contours) is not 0:
		max_index, max_area = max(enumerate([cv.contourArea(x) for x in contours]), key = lambda x: x[1])
		max_contour = contours[max_index]
		rect = cv.minAreaRect(max_contour)
		rect = cv.boxPoints(rect)

	return rect


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
	box = np.int0(box)
	box = sort_coords(box)

	w, h, c = img.shape
	rotM = cv.getRotationMatrix2D(center, np.degrees(phi), 1.0)
	img = cv.warpAffine(img, rotM, (int(h*1.4), int(w*1.4)))

	x = box[0][0]
	y = box[0][1]
	w = box[2][0] - box[0][0]
	h = box[1][1] - box[0][1]
	y += int(0.2 * h)
	h = int(0.6 * h)
	img = img[y:(y+h), x:(x+w)]

	return img


def simplify_image(img):
	#  kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
	#  img = cv.filter2D(img, -1, kernel)

	h, w, c = img.shape
	simple = np.zeros((10, w, 3), np.uint8)
	for i in range(w):
		sumB = 0
		sumR = 0
		sumG = 0
		for j in range(h):
			sumB += img[j, i, 0]
			sumR += img[j, i, 1]
			sumG += img[j, i, 2]

		for k in range(10):
			simple[k, i] = [ sumB/h, sumR/h, sumG/h ]

	N = 16;
	simple  /= N;
	simple  *= N;
	#  simple = cv.filter2D(simple, -1, kernel)
	return simple


def find_bands(img):
	i = 0
	hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV);
	h, w, c = img.shape

	#  while hsv[0, i][0] >= 0 and i < w:
	while i < w:
		check_color(hsv[0, i])
		i += 1


def check_color(px):
	print px

#  def check_color_range(h, s, v, col):
	#  if (h > col.lowH)


colors = {
	'black': {
		'lowH': 0,
		'highH': 179,
		'lowS': 0,
		'highS': 121,
		'lowV': 0,
		'highV': 57,
	},
	'brown': {
		'lowH': 3,
		'highH': 20,
		'lowS': 200,
		'highS': 255,
		'lowV': 80,
		'highV': 140,
	},
	'red': {
		'lowH': 170,
		'highH': 5,
		'lowS': 124,
		'highS': 255,
		'lowV': 74,
		'highV': 255,
	},
	'orange': {
		'lowH': 3,
		'highH': 20,
		'lowS': 200,
		'highS': 255,
		'lowV': 141,
		'highV': 255,
	},
	'yellow': {
		'lowH': 20,
		'highH': 30,
		'lowS': 190,
		'highS': 255,
		'lowV': 100,
		'highV': 200,
	},
	'green': {
		'lowH': 45,
		'highH': 80,
		'lowS': 120,
		'highS': 255,
		'lowV': 30,
		'highV': 150,
	},
	'blue': {
		'lowH': 90,
		'highH': 120,
		'lowS': 111,
		'highS': 255,
		'lowV': 50,
		'highV': 255,
	},
	'purple': {
		'lowH': 140,
		'highH': 169,
		'lowS': 100,
		'highS': 220,
		'lowV': 10,
		'highV': 150,
	},
	'gray': {
		'lowH': 0,
		'highH': 80,
		'lowS': 0,
		'highS': 85,
		'lowV': 100,
		'highV': 190,
	},
	'white': {
		'lowH': 0,
		'highH': 85,
		'lowS': 0,
		'highS': 30,
		'lowV': 150,
		'highV': 255,
	},
	'gold': {
		'lowH': 15,
		'highH': 30,
		'lowS': 160,
		'highS': 230,
		'lowV': 100,
		'highV': 200,
	},
}


if __name__ == "__main__":
	main()
