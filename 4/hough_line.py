# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 pavle <pavle.portic@tilda.center>
#
# Distributed under terms of the MIT license.

import sys
import math
import cv2 as cv
import os
import numpy as np

def main(argv):
	root = raw_input()
	#  root = 'set/example_4'
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
	print circle[0], circle[1], len(lines)/2, 0, 0, 0, 0

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
		return circles[0][0][0], circles[0][0][1]

	return 0, 0


if __name__ == "__main__":
	main(sys.argv[1:])

