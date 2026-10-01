#!usr/bin/python
# -*- coding: utf-8 -*-import string

import numpy as np

def distfct_circle(theta:np.ndarray, radius:float=1.0) -> np.ndarray:
	'''
	Polar representation of a circle with center point at (0,0): returns constant value for all theta.
	'''
	return np.asarray([radius for _ in theta])

def distfct_square(theta:np.ndarray, sidelength:float=1.0, rotation:float=0.0) -> np.ndarray:
	'''
	Polar representation of a square with center point (0,0).
	'''
	return sidelength / np.maximum(np.abs(np.cos(theta+rotation)), np.abs(np.sin(theta+rotation)))

### Piecewise-linear distance functions:
# generic function:
def piecewise_distance(theta:np.ndarray, fixpoints:np.ndarray) -> np.ndarray:
	'''
	A piecewise linear function.
	Function values are interpolated from fixpoints.
	
	theta:
		1D-array of input values
	
	fixpoints:
		2D-array of shape (n,2). Each row contains a pair of [theta, radius(theta).
		- Array is assumed to be ordered by theta.
	'''
	#print (theta)
	#print (fixpoints)
	
	# remove rows with nan or inf from fixpoints:
	fixpoints = fixpoints[~np.isnan(fixpoints).any(axis=1)]
	fixpoints = fixpoints[np.isfinite(fixpoints).all(axis=1)]
	
	# cover special case if input is a single float:
	if isinstance(theta, float):
		n = 1
		theta = np.asarray([theta])
	else:
		(n,_) = fixpoints.shape
	(m,) = theta.shape
	result = np.zeros(m)
	for t_i in range(m):
		# find the neighbors of theta[t_i] in the list of fixpoints
		# iterate through fixpoints via x_i until theta[t_i]-fixpoints[x_i,0] changes sign:
		# then fixpoints[x_i,0] and fixpoints[x_(i+1),0] are neighbors of theta[t_i]
		x_i = 0
		while x_i<n-1:
			if (theta[t_i]-fixpoints[x_i,0])*(theta[t_i]-fixpoints[x_i+1,0]) > 0:
				# both fixpoints are larger or both fixpoints are smaller
				x_i += 1
			else:
				# fixpoints[x_i] are fixpoints[x_i+1] neighbors of theta[t_i]
				break
		if x_i > 0 and x_i < n:
			# construct linear approximation of distance between two nearest fixpoints:
			dist_s = fixpoints[x_i-1,1]
			dist_t = fixpoints[x_i, 1]
			delta_s_t = fixpoints[x_i,0]-fixpoints[x_i-1,0]
			delta_s_theta = theta[t_i]-fixpoints[x_i-1,0]
			result[t_i] = dist_s + (delta_s_theta/delta_s_t)*(dist_t-dist_s)
		else:
			result[t_i] = np.inf
	return result

# piecewise linear distance-function defined by a list of points.
def construct_piecewise_distance_fct_from_Pointset(theta:np.ndarray, points:list):
	'''
	theta: float or ndarray of floats (input value)
	points: a list of Point.
	To work properly, points have to be sorted increasing with theta, starting at theta=0.
	'''
	fixpoints = np.stack([p.get_coordinates_polar() for p in points])
	return piecewise_distance(theta, fixpoints)