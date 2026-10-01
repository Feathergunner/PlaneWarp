#!usr/bin/python
# -*- coding: utf-8 -*-import string

import numpy as np
import matplotlib.pyplot as plt

from Shapes import ShapeConstructor
import DistanceFunctions as DF


def plot_transformation(shape, reference, transformed):
	'''
	Helper function that plots a transformation, before and after
	shape: the initial shape
	reference: the reference-shape of the transformation
	transformed: the transformed shape
	'''
	fig, ax = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw={"wspace": 0.1})
	ax[0].set_aspect("equal")
	ax[0].axis("off")
	ax[1].set_aspect("equal")
	ax[1].axis("off")
	
	# ax[0] is the "before" image:
	shape.plot(ax[0])
	reference.plot(ax[0], color='red', add_title=False, plot_background_grid=False)

	# ax[1] is the "after" image:
	transformed.plot(ax[1])
	reference.plot(ax[1], color='red', add_title=False, plot_background_grid=False)
	plt.tight_layout()
	plt.show()

def distfct_largecircle(theta):
	# a custom circle shape with larger radius than default
	return DF.distfct_circle(theta, radius=2.1)

if __name__ == '__main__':
	# initialize a ShapeConstructor for simplified shape construction:
	sc = ShapeConstructor()

	# define some shapes:
	circle = sc.construct_from_distancefct(DF.distfct_circle, name="circle")
	square = sc.construct_from_distancefct(DF.distfct_square, name="square")
	blossom = sc.construct_from_distancefct(DF.distfct_blossom, name="blossom")
	windrose = sc.construct_from_distancefct(DF.distfct_windrose, name="windrose")
	gear = sc.construct_from_distancefct(DF.distfct_gear, name="gear")
	largecircle = sc.construct_from_distancefct(distfct_largecircle, name="largecircle")

	# construct some transformed shapes and plot them:
	# mirror:
	shape_1 = square | largecircle
	plot_transformation(square, largecircle, shape_1)
	# fisheye-effect:
	shape_2 = windrose * circle
	plot_transformation(windrose, circle, shape_2)
	# scaling R^2 into the reference shape:
	shape_3 = gear ** blossom
	plot_transformation(gear, blossom, shape_3)