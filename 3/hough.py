#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 pavle <pavle.portic@tilda.center>
#
# Distributed under terms of the MIT license.

import cv2 as cv
import numpy as np

def main():
	filename = "set/A1.png"
	src = cv.imread(filename)
	#  dst = cv.Canny(src, 50, 200, None, 3)

	edges = cv.Canny(src, 20, 250, apertureSize = 3)
	lines = cv.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
	dest = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)

	for line in lines:
		x1,y1,x2,y2 = line[0]
		#  cv.line(dest, (x1, y1), (x2, y2), (0, 0, 255), 2)

	cv.imshow('Detected', dest)
	cv.waitKey()

	#  cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
	#  lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)

	#  if lines is not None:
		#  for i in [ 0 ]:
			#  rho = lines[i][0][0]
			#  theta = lines[i][0][1]
			#  a = np.cos(theta)
			#  b = np.sin(theta)
			#  x0 = a * rho
			#  y0 = b * rho
			#  pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
			#  pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
			#  cv.line(cdst, pt1, pt2, (0,0,255), 3, cv.LINE_AA)
			#  print type(lines)

	#  cv.imshow("Source", src)
	#  cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
	#  cv.waitKey()
	return 0


if __name__ == "__main__":
	main()
