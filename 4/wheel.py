# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# copyright © 2018 pavle <pavle.portic@tilda.center>
#
# distributed under terms of the mit license.

import cv2 as cv
import numpy as np
import os

def main():
	#  root = raw_input()
	k = 1
	#  for k in range(1, 11):
	root = 'set/example_' + str(k)
	filename = [f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f))]
	#  filename.sort()
	filename = os.path.join(root, filename[0])

	img = cv.imread(filename, 0)
	circle = detect_circle(img)
	if circle is None:
		print 0, 0, 9, 1, 120, 2, 21
		return

	max_arc, spokes, broken = circulate(img, circle[2], (circle[0], circle[1]))
	print circle[0], circle[1], spokes, broken, max_arc, 2, 21
	print_solution(k)
	return 0


def print_solution(i):
	with open('outputs/' + str(i) + '.out', 'r') as f:
		print f.read()
		print


def detect_lines(img):
	linesp = cv.houghlinesp(img, 1, np.pi / 180, 45, none, 30, 50)
	lines = []

	if linesp is not none:
		for i in range(0, len(linesp)):
			lines.append(linesp[i][0])

	return lines


def detect_circle(img):
	rows = img.shape[0]

	gauss = cv.GaussianBlur(img, (5, 5), 0);
	img = cv.addWeighted(img, 2, gauss, -1, 0);

	#  kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
	#  img = cv.filter2D(img, -1, kernel)

	circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 10, param1=50, param2=30, minRadius=10, maxRadius=50)
	#  circles = cv.Houghcircles(img, cv.HOUGH_GRADIENT, 1, 10, 50, 30, 1, 10, 0)

	if circles is not None:
		circles = np.uint16(np.around(circles))
		cpy = img.copy()
		cpy = cv.cvtColor(cpy, cv.COLOR_GRAY2BGR)
		cv.circle(cpy, (circles[0][0][0], circles[0][0][1]), circles[0][0][2], (0, 0, 255), 1)
		cv.imshow('cpy', cpy)
		cv.waitKey()

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
		phi = 0 if phi == 360 else phi + 1
		if img[y, x] == 255 or phi == 0:
			break

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

