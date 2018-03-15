# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 pavle <pavle.portic@tilda.center>
#
# Distributed under terms of the MIT license.

import numpy as np
import os

def main():
	os.chdir(raw_input())
	files = get_files()
	files.sort()

	for file in files:
		with open(file) as f:
			i = 0
			for line in f:
				coords = calculate_coordinates(line)
				print file, i, coords[0], coords[1]
				i += 1
			f.close()


def get_files():
	out = []
	for root, dirs, files in os.walk('.'):
		for file in files:
			out.append(os.path.join(root[2:], file))

	return out


def calculate_coordinates(numbers):
	numbers = numbers.split()
	numbers = [ float(x) for x in numbers ]
	O = (numbers[0], numbers[1])
	X = tuple(np.subtract((numbers[2], numbers[3]), O))
	Y = tuple(np.subtract((numbers[4], numbers[5]), O))
	A = tuple(np.subtract((numbers[6], numbers[7]), O))

	phi = -get_angle(X)

	sin = np.sin(phi)
	cos = np.cos(phi)
	Y = rotate_pt(Y, sin, cos)
	A = rotate_pt(A, sin, cos)

	if round(np.degrees(get_angle(Y))) == -90.0:
		A = (A[0], -A[1])

	return (round(A[0], 4), round(A[1], 4))


def get_angle(points):
	return np.arctan2(points[1], points[0])


def rotate_pt(pt, sin, cos):
	return (pt[0]*cos - pt[1]*sin, pt[1]*cos + pt[0]*sin)


if __name__ == "__main__":
	main()
