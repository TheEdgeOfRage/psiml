# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 pavle <pavle.portic@tilda.center>
#
# Distributed under terms of the MIT license.
# set/example_

import cv2 as cv
import numpy as np
import os

def main():
	root = raw_input()
	filename = [f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f))]
	filename.sort()
	filename = filename[0]
	detect_circle(os.path.join(root, filename))


def detect_circle(filename):
	src = cv.imread(filename, cv.IMREAD_COLOR)

	gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
	rows = gray.shape[0]
	circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows/16, 100, 100, 30, 1, 50)

	if circles is not None:
		circles = np.uint16(np.around(circles))
		print circles[0][0][0], circles[0][0][1], 0, 0, 0, 0, 0


if __name__ == "__main__":
	main()

