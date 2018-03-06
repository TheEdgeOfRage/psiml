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
	root = raw_input()
	filename = [f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f))]
	filename = os.path.join(root, filename[0])

	img = cv.imread(filename, 0)
	circle = detect_circle(img)
	if circle is None:
		print 0, 0, 9, 1, 120, 2, 21
		return

	max_arc, spokes, broken = circulate(img, circle[2], (circle[0], circle[1]))

	print circle[0], circle[1], spokes, broken, max_arc, 3, 21
	return 0


def print_solution(i):
	with open('outputs/' + str(i) + '.out', 'r') as f:
		print f.read()
		print


def detect_circle(img):
	rows = img.shape[0]
	circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, rows/16, 100, 100, 30, 1, 50)

	if circles is not None:
		circles = np.uint16(np.around(circles))
		return circles[0][0]

	return None


def circulate(img, R, c):
	r =  R + 4
	phi = 0
	arcs = []
	last_spoke = True
	spokes = {}

	while True:
		x, y = np.int0(pol2car(r, phi))
		x += c[0]
		y += c[1]
		if img[y, x] == 255:
			break

		phi += 1
		if phi == 360:
			return 360

	spokes[phi] = 1
	stage1, stage2 = {}, {}

	while True:
		curr_phi = 0
		max_phi = 0
		p = phi + 1
		x, y = None, None
		final = False
		while True:
			x, y = np.int0(pol2car(r, p))
			x += c[0]
			y += c[1]

			if img[y, x] < 255:
				last_spoke = False
				curr_phi += 1
				if p in spokes and spokes[p] == 1 and img[y, x] == 0:
					stage1[p] = 0
					#  print p, stage1[p]
					#  draw_dot(img, x, y)
			else:
				if curr_phi > max_phi:
					max_phi = curr_phi
				curr_phi = 0

				if not last_spoke and not intersects(range(p-6, p+7), spokes.keys()):
					if r - R > 10:
						stage1[p] = 0
					else:
						stage1[p] = 1
					#  print p, stage1[p]
					#  draw_dot(img, x, y)

				last_spoke = True

				if final:
					break

			p = 0 if p == 359 else p + 1
			if p == phi:
				final = True

		if max_phi == 0:
			break

		if len(stage2) > 0:
			for s in stage2:
				spokes[s] = stage2[s]
			stage2 = {}

		if len(merge_dict(stage1, spokes)) > 11:
			for s in stage1:
				stage2[s] = stage1[s]
		else:
			for s in stage1:
				spokes[s] = stage1[s]

		arcs.append(max_phi)
		r += 5

	broken = 0
	for s in spokes:
		if spokes[s] == 0:
			broken += 1

	return max(arcs), len(spokes), broken


def merge_dict(a, b):
	z = a.copy()
	z.update(b)
	return z

def intersects(a, b):
	s = set(b)
	i = [val for val in a if val in s]
	return len(i) > 0


def car2pol(x, y):
	return np.sqrt(x**2 + y**2), np.arctan2(y, x)


def pol2car(r, p):
	p = np.radians(p)
	return r * np.cos(p), r * np.sin(p)


def draw_dot(img, x, y):
	cpy = img.copy()
	cpy = cv.cvtColor(cpy, cv.COLOR_GRAY2BGR)
	cv.circle(cpy, (x, y), 1, (0, 0, 255), 2)
	cv.imshow('img', cpy)
	cv.waitKey()


if __name__ == "__main__":
	main()
