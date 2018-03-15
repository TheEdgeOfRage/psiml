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
import itertools as it
import numpy as np


def main():
	#  for k in range(10, 11):
	#  filename = 'set/A' + str(k) + '.png'
	#  filename = raw_input()
	#  src = cv.imread(filename)
	#  wrapper(src)

	#  i = 9
	for i in range(2, 11):
		filename = 'private/set/B' + str(i) + '.png'
		src = cv.imread(filename)
		wrapper(src)
		cv.waitKey()
		print_solution(i)


def wrapper(src):
	src = filter_pink(src)
	box = find_resistor(src)
	if box is None:
		print '221G'
		return

	src = crop_resistor(src, box)
	if len(src) is 0:
		print '221G'
		return

	simple = simplify_image(src)
	code = find_bands(simple)
	if code is '':
		print '221G'
		return

	if code[0] is 'G':
		code = code[::-1]

	code = code.replace('G', '') + '222'
	code = code[:3] + 'G'
	print code


def print_solution(i):
	with open('private/outputs/B' + str(i) + '.txt', 'r') as f:
		print f.read()
		print


def filter_pink(img):
	hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
	low = np.array([165, 0, 160])
	high = np.array([180, 170, 255])
	mask = cv.inRange(hsv, low, high)
	mask = cv.bitwise_not(mask)
	return cv.bitwise_and(img, img, mask=mask)


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
	src = img.copy()
	img = contrast(img, 1.6)
	img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	img = cv.medianBlur(img, 21)
	img = cv.Canny(img, 60, 100)

	kernel = np.ones((9, 9), np.uint8)
	img = cv.dilate(img, kernel, 2)
	img = cv.erode(img, kernel, 2)
	img, contours, _ = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	rect = None

	if len(contours) is not 0:
		ind, _ = max(enumerate([cv.contourArea(x) for x in contours]), key = lambda x: x[1])
		max_contour = contours[ind]
		rect = cv.minAreaRect(max_contour)
		rect = cv.boxPoints(rect)
		#  cv.drawContours(src, [np.int0(rect)], 0, (0, 0, 255), 2)
		#  cv.imshow('src', src)

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
	x += int(0.1 * w)
	w = int(0.8 * w)
	img = img[y:(y+h), x:(x+w)]
	#  cv.imshow('img', img)

	return img


def simplify_image(img):
	#  kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
	#  img = cv.filter2D(img, -1, kernel)

	h, w, c = img.shape
	simple_height = 5
	simple = np.zeros((simple_height, w, 3), np.uint8)
	for i in range(w):
		sumB = 0
		sumR = 0
		sumG = 0
		for j in range(h):
			sumB += img[j, i, 0]
			sumR += img[j, i, 1]
			sumG += img[j, i, 2]

		for k in range(simple_height):
			simple[k, i] = [ sumB/h, sumR/h, sumG/h ]

	return simple


def find_bands(img):
	i = 0
	hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV);
	h, w, c = img.shape

	#  check_color(hsv[0, 0])
	#  while hsv[0, i][0] >= 0 and i < w:
	band_colors = []
	for i in range(w):
		#  print i, hsv[0, i]
		band_colors.append(check_color(hsv[0, i]))

	band_colors = [k for k, g in it.groupby(band_colors) if sum(1 for _ in g) > 2]
	band_colors = filter(None, band_colors)
	return ''.join(band_colors)


def check_color(px):
	pColors = {}
	pColors['0'] = np.mean(check_color_range(px[0], px[1], px[2], 'black') or[ 0 ])
	pColors['1'] = np.mean(check_color_range(px[0], px[1], px[2], 'brown') or[ 0 ])
	pColors['2'] = np.mean(check_color_range(px[0], px[1], px[2], 'red') or[ 0 ])
	pColors['3'] = np.mean(check_color_range(px[0], px[1], px[2], 'orange') or[ 0 ])
	pColors['4'] = np.mean(check_color_range(px[0], px[1], px[2], 'yellow') or[ 0 ])
	pColors['5'] = np.mean(check_color_range(px[0], px[1], px[2], 'green') or[ 0 ])
	pColors['6'] = np.mean(check_color_range(px[0], px[1], px[2], 'blue') or[ 0 ])
	pColors['7'] = np.mean(check_color_range(px[0], px[1], px[2], 'purple') or[ 0 ])
	pColors['8'] = np.mean(check_color_range(px[0], px[1], px[2], 'gray') or[ 0 ])
	pColors['9'] = np.mean(check_color_range(px[0], px[1], px[2], 'white') or[ 0 ])
	pColors['G'] = np.mean(check_color_range(px[0], px[1], px[2], 'gold') or[ 0 ])
	best = max(pColors, key=pColors.get)
	best = None if pColors[best] < 0.05 else best
	return best


def check_color_range(h, s, v, color_str):
	col = colors[color_str]
	if color_str == 'red':
		if ((h >= col['lowH'] and h <= 0) or (h >= 0 and h <= col['highH'])) and s >= col['lowS'] and s <= col['highS'] and v >= col['lowV'] and v <= col['highV']:
			diff = 180 - col['lowH']
			h = calculate_offset(h + diff, col['highH'] + diff, 0)
			s = calculate_offset(s, col['highS'], col['lowS'])
			v = calculate_offset(v, col['highV'], col['lowV'])
			return [h, s, v]
	else:
		if h >= col['lowH'] and h <= col['highH'] and s >= col['lowS'] and s <= col['highS'] and v >= col['lowV'] and v <= col['highV']:
			h = calculate_offset(h, col['highH'], col['lowH'])
			s = calculate_offset(s, col['highS'], col['lowS'])
			v = calculate_offset(v, col['highV'], col['lowV'])
			return [h, s, v]
	return None


def calculate_offset(x, high, low):
	m = (high - low) / 2.0
	return 1 - abs((x - m) / (high - m))


colors = {
	'black': {
		'lowH': 0,
		'highH': 179,
		'lowS': 0,
		'highS': 10,
		'lowV': 0,
		'highV': 40,
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
		'highH': 32,
		'lowS': 180,
		'highS': 255,
		'lowV': 100,
		'highV': 230,
	},
	'green': {
		'lowH': 40,
		'highH': 80,
		'lowS': 60,
		'highS': 255,
		'lowV': 30,
		'highV': 255,
	},
	'blue': {
		'lowH': 81,
		'highH': 125,
		'lowS': 40,
		'highS': 255,
		'lowV': 30,
		'highV': 255,
	},
	'purple': {
		'lowH': 140,
		'highH': 175,
		'lowS': 170,
		'highS': 255,
		'lowV': 10,
		'highV': 210,
	},
	'gray': {
		'lowH': 0,
		'highH': 40,
		'lowS': 0,
		'highS': 83,
		'lowV': 100,
		'highV': 220,
	},
	'white': {
		'lowH': 0,
		'highH': 40,
		'lowS': 0,
		'highS': 15,
		'lowV': 221,
		'highV': 255,
	},
	'gold': {
		'lowH': 10,
		'highH': 20,
		'lowS': 150,
		'highS': 230,
		'lowV': 100,
		'highV': 175,
	},
}


if __name__ == "__main__":
	main()
