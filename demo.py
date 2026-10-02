#!usr/bin/python
# -*- coding: utf-8 -*-import string

import numpy as np
import matplotlib.pyplot as plt

from Shapes import ShapeConstructor
import DistanceFunctions as DF

def quickstart():
	'''
	To define a shape, use a ShapeConstructor
	'''
	from Shapes import ShapeConstructor
	sc = ShapeConstructor()
	'''
	and then create a shape-object, for example using one of the pre-defined distance-functions (these are functions f:(0,2*pi)->R that map radians to angles, thus defining the outline of a shape in polar coordinates). For example, a windrose:
	'''
	import DistanceFunctions as DF
	windrose = sc.construct_from_distancefct(DF.distfct_windrose, name="windrose")
	'''
	You don't have to specify a name, but the name of the shape can be used for plot titles.
	
	Now to transform our windrose-shape into something fancy, we need to choose a transformation and a second shape to specify the scope of the transformation.
	Let's implement a fisheye-effect on the interior of a square:
	'''
	square = sc.construct_from_distancefct(DF.distfct_square, name="square")
	'''
	And now, applying the transformation is straightforward, since the transformations are implemented as operators of shapes:
	'''
	fancy_fisheye_windrose = windrose*square
	'''
	Now all that's left is to plot our transformed shape.
	To this end, we only need to initialize a matplotlib-figure and get the axes-element.
	With this, we can simply tell our shape to go plot itself on the axes:
	'''
	from matplotlib import pyplot as plt
	ax = plt.gca()
	fancy_fisheye_windrose.plot(ax)
	plt.show()
	

def create_simple_examples():
	'''
	Create three simple examples of plane warping.
	'''
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


def create_fancy_image():
	'''
	See function name.

	This is slightly more complex than the simple examples,
	so consider create_simple_examples first to understand what's going on.
	'''

	# define a set of similar shapes with increasing size:
	# (a custom blossom-shape with 7 leaves)
	def distfuct_blossom7_1(theta):
		return DF.distfct_blossom(theta, min_rad=0.1, max_rad = 0.5, num_rays=7, rotation=0.5*np.pi)
	def distfuct_blossom7_2(theta):
		return DF.distfct_blossom(theta, min_rad=0.2, max_rad = 0.75, num_rays=7, rotation=0.5*np.pi)
	def distfuct_blossom7_3(theta):
		return DF.distfct_blossom(theta, min_rad=0.3, max_rad = 1.0, num_rays=7, rotation=0.5*np.pi)
	def distfuct_blossom7_4(theta):
		return DF.distfct_blossom(theta, min_rad=0.4, max_rad = 1.25, num_rays=7, rotation=0.5*np.pi)
	def distfuct_blossom7_5(theta):
		return DF.distfct_blossom(theta, min_rad=0.5, max_rad = 1.5, num_rays=7, rotation=0.5*np.pi)
	blossom_fcts = [distfuct_blossom7_1, distfuct_blossom7_2, distfuct_blossom7_3, distfuct_blossom7_4, distfuct_blossom7_5]

	# Construct a set of basic shapes with increasing size:
	sc = ShapeConstructor()
	blossom_shapes = [sc.construct_from_distancefct(blossom_fcts[i], name="b"+str(i+1)) for i in range(5)]

	# Construct a reference shape:
	def distfct_gear(theta):
		return DF.distfct_gear(theta, rotation=np.pi/16)
	reference = sc.construct_from_distancefct(distfct_gear, name="reference")

	# compute warped shapes:
	warped_shapes = [blossom**reference for blossom in blossom_shapes]

	# initialize plot:
	colors = ["purple", "red", "orange", "yellow", "green"]
	num_subplots = 3
	fig, ax = plt.subplots(1, num_subplots, figsize=(5*num_subplots, 5), gridspec_kw={"wspace": 0.1})
	for i in range(num_subplots):
		ax[i].set_aspect("equal")
		ax[i].axis("off")
	# plot images:
	# plot original shapes at first subplot:
	for i in range(5):
		blossom_shapes[i].plot(ax[0], color=colors[i], plot_background_grid=i==0, add_title=False)
	ax[0].set_title("Original image with cartesian grid")

	# plot only the warped grid and outline at second subplot:
	warped_shapes[0].plot_grid(ax[1])
	reference.plot(ax[1], color='black', plot_background_grid=False, add_title=False)
	ax[1].set_title("The grid after projecting R^2 into the gear-shape")

	# plot the warped_shape at third subplot:
	for i in range(5):
		warped_shapes[i].plot(ax[2], color=colors[i], plot_background_grid=False, add_title=False)
	ax[2].set_title("The warped image")

	plt.show()

	# Aaaaand a second warp:
	# construct another reference shape:
	def distfct_smallsquare(theta):
		return DF.distfct_square(theta, sidelength=0.5)
	reference_2 = sc.construct_from_distancefct(distfct_smallsquare, name="reference_2")
	warped_shapes_2 = [shape|reference_2 for shape in warped_shapes]

	# initialize plot:
	num_subplots = 3
	fig, ax = plt.subplots(1, num_subplots, figsize=(5*num_subplots, 5), gridspec_kw={"wspace": 0.1})
	for i in range(num_subplots):
		ax[i].set_aspect("equal")
		ax[i].axis("off")

	# plot image after first warp with second reference shape at first subplot:
	for i in range(5):
		warped_shapes[i].plot(ax[0], color=colors[i], plot_background_grid=i==0, add_title=False)
		ax[0].set_title("Image before second warp with new reference shape")
	reference_2.plot(ax[0], color='black', plot_background_grid=False, add_title=False)

	# plot only the warped grid and outline at second subplot:
	warped_shapes_2[0].plot_grid(ax[1])
	reference_2.plot(ax[1], color='black', plot_background_grid=False, add_title=False)
	ax[1].set_title("The two-times-warped space")

	for i in range(5):
		# plot the warped_shape at third subplot:
		warped_shapes_2[i].plot(ax[2], color=colors[i], plot_background_grid=False, add_title=False)
	ax[2].set_title("The two-times warped image")

	plt.show()

if __name__ == '__main__':
	quickstart()
	#create_simple_examples()
	#create_fancy_image()