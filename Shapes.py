#!usr/bin/python
# -*- coding: utf-8 -*-import string

import numpy as np
import matplotlib.pyplot as plt

import Transformations

class ShapeConstructor:
	'''
	Class to handle shape construction
	'''
	def construct_grid(self, x_min:float=-2.0, x_max:float=2.0, y_min:float=-2.0, y_max:float=2.0, spacing:float=0.25, n:int=100) -> list:
		'''
		Helper function that constructs a list of Shapes which define a regular grid.

		x_min, x_max, y_min, y_max: float
			define size of grid.
		spacing: float
			defines distance between gridlines.
		n: int
			defines number of points on each gridline. To plot the grid in cartesian coordinates, n=2 is sufficient
			(gives startpoint and endpoint for each straight gridline).
			However, if the grid is transformed by some projection, a higher resolution is necessary to correctly represent the warped gridlines.
		'''
		gridlines = []
		xs = np.linspace(x_min, x_max, n)
		for y in np.arange(y_min, x_max+spacing, spacing):
			gridlines.append(self.construct_from_points_cartesian(np.asarray([[x_, y] for x_ in xs]), "gly="+str(y)))
			# np.column_stack((xs, np.full(n, y)))
		ys = np.linspace(y_min, y_max, n)
		for x in np.arange(x_min, x_max+spacing, spacing):
			gridlines.append(self.construct_from_points_cartesian(np.asarray([[x, y_] for y_ in xs]), "glx="+str(x)))
			#np.column_stack((np.full(n, x), ys))),"glx="+str(x))
		return gridlines
	
	def construct_from_points_polar(self, points_polar:np.ndarray, name:str="", add_grid:bool=False):
		'''
		Constructs a Shape from a set of points given in polar coordinates.

		points_polar: np.ndarray of shape (2,n)
			that contains n points defines by (theta, radius)
		
		name: str
			specifies a name to represent the shape (e.g. for plot captions)

		add_grid: bool
			if true, a background grid is added to the shape.
		'''
		grid = None
		if add_grid:
			grid = self.construct_grid()
		return Shape(points_polar, name, grid)
	
	def construct_from_points_cartesian(self, points_cartesian:np.ndarray, name:str="", add_grid:bool=False):
		'''
		Constructs a Shape from a set of points given in cartesian coordinates.

		points_cartesian: np.ndarray of shape (2,n)
			that contains n points defines by (x,y)
		
		name: str
			specifies a name to represent the shape (e.g. for plot captions)

		add_grid: bool
			if true, a background grid is added to the shape.
		'''
		#print ("input cartesian:", points_cartesian)
		points_polar = np.transpose(np.asarray([
			np.arctan2(points_cartesian[:,1], points_cartesian[:,0]),
			np.sqrt(points_cartesian[:,1]**2 + points_cartesian[:,0]**2)]))
		#print ("output polar:", points_polar)
		return self.construct_from_points_polar(points_polar, name, add_grid)
	
	def construct_from_distancefct(self, distancefct, resolution:int=630, name:str="", add_grid:bool=False):
		'''
		Constructs a Shape from a distance function, i.e. a function that defines the distance to (0,0) given an angle theta.

		distancefct: Callable
			a function that takes an np.ndarray of shape (n) (a list of angles theta) and
			 returns an np.ndarray of shape (n) (a list of distances at the corresponding angles).
		
		resolution: int
			defines how many points are constructed from the distancefct for initializing the shape.

		name: str
			specifies a name to represent the shape (e.g. for plot captions)

		add_grid: bool
			if true, a background grid is added to the shape.
		'''
		grid = None
		if add_grid:
			grid = self.construct_grid()
		theta = np.linspace(0, 2*np.pi, resolution)
		radius = distancefct(theta)
		points_polar = np.column_stack((theta, radius))
		return Shape(points_polar, name, grid, distancefct)

class Shape:
	'''
	Class to represent 2D-lines that can be morphed by a projection of R^2 onto (a subset of) R^2.
	(These projections are parameterized by a Shape that defines the scope of the projection.)

	Shapes are represented by a list of points in polar coordinates.

	Shapes can have a background-grid, which is again a set of Shapes.
	The grid is morphed together with the main shape, this can by used to visualize the projection.
	'''
	def __init__(self, _points_polar:np.ndarray, _name:str, _background_grid:list=None, _distancefct=None):
		# name of the shape (for generated filenames etc.):
		self.name = _name
		
		# a ndarray of shape (2,n) that contains n points in polar coordinates (theta, radius) which define the shape
		self.points = _points_polar
		
		## only if shape has a distance-function, it counts as "complete" i.e. encircles the (0,0)-point.
		## only these shapes qualify for beeing used as reference for transformations
		self.distancefct = _distancefct
		
		# background_grid: A list of Shapes.
		# It is inteded that each Shapes represents a straight line and all Shapes together form a regular grid.
		# This grid that can be visualised with the main shape (i.e. self.pojnts).
		# All transformations applied to the main Shape are also applied to the grid,
		# Therefore the (initially regular) grid helps visualizing the transformations.
		self.has_background_grid = not (_background_grid is None)
		self.background_grid = _background_grid
	
	def __str__(self):
		return "Shape '"+self.name+"'"
		
	def get_points(self) -> np.ndarray:
		return self.points
		
	def get_theta_range(self):
		return self.points[:,0]
	
	def get_radius_range(self):
		return self.points[:,1]
	
	### projections:
	def _apply_transformation(self, other, transformation_fct):
		'''
		Applies a given transformation_fct with resprect to a reference-Shape to self.

		other: Shape
			the reference-Shape that defines the scope of the transformation.
			The reference-Shape has to have a distancefct, because it has to be ensured that the reference fully encircles the (0,0)-point.
		'''
		## check that other.distancefct is not None, raise exception if None
		if other.distancefct is None:
			raise Exception("Shape other has to have a distancefct")
		theta = self.get_theta_range()
		radius = self.get_radius_range()

		radius_other = other.distancefct(theta)
		radius_transformed = transformation_fct(radius, radius_other)
		#print ("compute fixpoints...")
		#print ("radius:",radius)
		#print ("radius_other:",radius_other)
		#print ("radius_transformed:", radius_transformed)
		morphed_points = np.concatenate((theta[:,None], radius_transformed[:,None]),axis=1)
		#print ("morphed points:",morphed_points)
		return morphed_points
	
	def __or__(self, other):
		'''
		define the | operator to implement mirroring along the boundary of the other Shape
		'''
		transformed_points = self._apply_transformation(other, Transformations.mirror)
		transformed_name = self.name+"|"+other.name
		transformed_grid = None
		if self.has_background_grid:
			transformed_grid = [gridline|other for gridline in self.background_grid]
		return Shape(transformed_points, transformed_name, transformed_grid)
	
	def __mul__(self, other):
		'''
		define the * operator to implement the fish-eye-effect in the interior of the other Shape
		'''
		transformed_points = self._apply_transformation(other, Transformations.fisheye)
		transformed_name = self.name+"*"+other.name
		transformed_grid = None
		if self.has_background_grid:
			transformed_grid = [gridline*other for gridline in self.background_grid]
		return Shape(transformed_points, transformed_name, transformed_grid)
	
	def __pow__(self, other):
		'''
		define the ** operator to implement the scaling of R^2 into the interior of the other Shape
		'''
		transformed_points = self._apply_transformation(other, Transformations.scale)
		transformed_name = self.name+"**"+other.name
		transformed_grid = None
		if self.has_background_grid:
			transformed_grid = [gridline**other for gridline in self.background_grid]
		return Shape(transformed_points, transformed_name, transformed_grid)
	
	### plotting
	
	def get_pointcoordinates_cartesian(self) -> np.ndarray:
		# compute cartesian coordinates from polar points
		points_cartesian = np.column_stack((
			self.get_radius_range() * np.cos(self.get_theta_range()),
			self.get_radius_range() * np.sin(self.get_theta_range())))
		#print ("cartesian points:", points_cartesian)
		return points_cartesian
	
	def plot(self, axes, color:str='black', linewidth:float=1.0, plot_background_grid:bool=True, add_title:bool=True) -> None:
		'''
		Plots the list of self.points on a specified axes of a matplotlib-figure.
		'''
		if self.has_background_grid and plot_background_grid:
			# plot background grid:
			for gridline in self.background_grid:
				gridline.plot(axes, color='blue', linewidth=0.1)
		cartesian_coordinates = self.get_pointcoordinates_cartesian()
		#print ("coords:", cartesian_coordinates)
		axes.plot(cartesian_coordinates[:,0], cartesian_coordinates[:,1], color, linewidth)
		if add_title:
			axes.set_title(self.name)
	
	def debug_plot_distance_fct(self, axes) -> None:
		'''
		Plots self.points directly in cartesian coordinates, visualizing radius(theta) as an x-y-plot.
		'''
		theta = self.get_theta_range()
		radius = self.get_radius_range()
		axes.plot(theta, radius)
