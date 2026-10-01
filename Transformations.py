#!usr/bin/python
# -*- coding: utf-8 -*-import string

import numpy as np

### functions that compute transformations of the radius of a point in polar coordinates:

def mirror(radius:float, radius_reference:float) -> float:
	'''
	Mirrors points at the reference distance, along the ray going through (0,0).
	Note that this considers the reference line only point-wise, it ignores the angles.
	This implements a correct mirror effect if and only if the reference is a circle.
	'''
	return 2*radius_reference-radius

def fisheye(radius:float, radius_reference:float) -> float:
	'''
	Implements a fish-eye-effect by stretching the space around (0,0)
	and compressing the space near the boundary of the reference shape (from the inside).
	Keeps everything outside the reference shape unaltered.
	'''
	x = radius/radius_reference
	if isinstance(radius, float):
		if radius > radius_reference:
			return radius
		else:
			return (1-(x-1)**2)
	else:
		return np.where(
			radius > radius_reference,
			radius,
			(radius_reference-(x-1)**2))

def scale(radius:float, radius_reference:float) -> float:
	'''
	Compresses all of R^2 into the reference shape.
	Maps (0,0) to (0,0) and infinity to the boundary of the reference shape.
	Near to (0,0), space is almost unaffected, but space gets more compressed the further away from (0,0).
	'''
	return radius_reference*np.tanh(radius)