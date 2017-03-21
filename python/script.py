from scipy import misc
import numpy as np
import cv2
import matplotlib.pyplot as plt

TILE_WIDTH = 16
MAP_WIDTH = 35
FILE_NAME = "wang_tiles.png"



def load_tileset(file_name):
	"""
	returns list of 3x3 numpy arrays.
	file_name: name of image file containing tile set
	"""
	image = cv2.cvtColor(cv2.imread(file_name), cv2.COLOR_BGR2RGB)
	image_width = image.shape[1]
	image_height = image.shape[0]
	print image.shape
	for x in range(0,image_width,4):
		for y in range(0,image_height,4):
			if not (image [x,y]==np.array([255,255,255])).all():
				print image [x,y]
				plt.imshow(image [x:x+4,y:y+4],interpolation='none')
				plt.show()













tileset = load_tileset(FILE_NAME)


def multi_image_example():
	methods = [None, 'none', 'nearest', 'bilinear', 'bicubic', 'spline16',
	           'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
	           'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos']

	grid = np.random.rand(4, 4)

	fig, axes = plt.subplots(3, 6, figsize=(12, 6),
	                         subplot_kw={'xticks': [], 'yticks': []})

	fig.subplots_adjust(hspace=0.3, wspace=0.05)

	for ax, interp_method in zip(axes.flat, methods):
	    ax.imshow(grid, interpolation=interp_method)
	    ax.set_title(interp_method)

	plt.show()