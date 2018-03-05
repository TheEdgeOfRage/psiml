# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 pavle <pavle.portic@tilda.center>
#
# Distributed under terms of the MIT license.

import cv2 as cv
import numpy as np
import os

def main():
	#  root = raw_input()
	root = 'set/example_4'
	filename = [f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f))]
	filename.sort()
	filename = os.path.join(root, filename[0])

	src = cv.imread(filename)
	img = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

	canny = cv.Canny(img, 50, 200, None, 3)
	lines = detect_lines(canny)
	for l in lines:
		cv.line(src, (l[0], l[1]), (l[2], l[3]), (0,0,255), 1, cv.LINE_AA)

	circle = detect_circle(img)

	arc = measure_arc(img, circle[2], (circle[0], circle[1]))

	print circle[0], circle[1], len(lines)/2, 0, arc, 0, 0

	#  cv.imshow("Probabilistic Line Transform", src)
	#  cv.imshow("Canny", canny)
	#  cv.waitKey()

	return 0


def detect_lines(img):
	linesP = cv.HoughLinesP(img, 1, np.pi / 180, 45, None, 30, 50)
	lines = []

	if linesP is not None:
		for i in range(0, len(linesP)):
			lines.append(linesP[i][0])

	return lines


def detect_circle(img):
	rows = img.shape[0]
	circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, rows/16, 100, 100, 30, 1, 50)

	if circles is not None:
		circles = np.uint16(np.around(circles))
		return circles[0][0]

	return [0, 0, 0]


def measure_arc(img, r, c):
	r += 2
	phi = 10

	while True:
		x, y = np.int0(pol2car(r, phi))
		x += c[0]
		y += c[1]
		if img[y, x] > 128:
			break

		phi += 2
		if phi == 360:
			return 360

	arcs = []
	while True:
		curr_phi = 0
		max_phi = 0
		p = phi + 1
		while True:
			x, y = np.int0(pol2car(r, p))
			x += c[0]
			y += c[1]

			if img[y, x] < 255:
				curr_phi += 1
			else:
				if curr_phi > max_phi:
					max_phi = curr_phi
				curr_phi = 0

			if p == phi:
				break

			#  print curr_phi
			#  copy = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
			#  cv.circle(copy, (x, y), 1, (0, 0, 255), 2)
			#  cv.imshow("rotate", copy)
			#  cv.waitKey()

			p += 1
			if p >= 360:
				p = 0


		if max_phi == 0:
			break

		arcs.append(max_phi)
		r += 5

	return max(arcs)


def car2pol(x, y):
	return np.sqrt(x**2 + y**2), np.arctan2(y, x)


def pol2car(r, p):
	p = np.radians(p)
	return r * np.cos(p), r * np.sin(p)


if __name__ == "__main__":
	main()

