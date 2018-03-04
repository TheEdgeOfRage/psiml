#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 pavle <pavle.portic@tilda.center>
#
# Distributed under terms of the MIT license.

"""
@file hough_lines.py
@brief This program demonstrates line finding with the Hough transform
"""
import sys
import math
import cv2 as cv
import numpy as np
def main(argv):
	default_file =  "set/A6.png"
	filename = argv[0] if len(argv) > 0 else default_file
	# Loads an image
	src = cv.imread(filename, cv.IMREAD_GRAYSCALE)
	# Check if image is loaded fine
	if src is None:
		print ('Error opening image!')
		print ('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
		return -1

	dst = cv.Canny(src, 50, 200, None, 3)

	# Copy edges to the images that will display the results in BGR
	cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
	lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)

	if lines is not None:
		#  for i in range(0, len(lines)):
		for i in [ 0 ]:
			rho = lines[i][0][0]
			theta = lines[i][0][1]
			a = math.cos(theta)
			b = math.sin(theta)
			x0 = a * rho
			y0 = b * rho
			pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
			pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
			cv.line(cdst, pt1, pt2, (0,0,255), 3, cv.LINE_AA)
	print type(lines)

	cv.imshow("Source", src)
	cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
	cv.waitKey()
	return 0

if __name__ == "__main__":
	main(sys.argv[1:])
