import cv2 as cv
import numpy as np

images = ['set/A1.png','set/A2.png','set/A3.png','set/A4.png','set/A5.png','set/A6.png','set/A7.png','set/A8.png','set/A9.png','set/A10.png']


def main():
	i = images[4]
	img = cv.imread(i, 0)

	kernel = np.ones((5,5),np.uint8)
	closing = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)

	cv.imshow("Closing", closing)
	cv.imshow("Source", img)
	cv.waitKey()


def rotateImage(image, angle):
	image_center = tuple(np.array(image.shape)/2)
	rot_mat = cv.getRotationMatrix2D(image_center,angle,1.0)
	result = cv.warpAffine(image, rot_mat, image.shape,flags=cv.INTER_LINEAR)
	return result


if __name__ == "__main__":
	main()

