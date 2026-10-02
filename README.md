# Plane Warp
This is a small Python project for experimenting with transformations of the 2D plane.

2D-Shapes can be easily defined and then transformed by mappings, such as a fisheye-effect. The mappings are in turn parameterized by another shape, e.g. the fisheye-effect is parameterized by a reference-shape which defines the area of the effect (in the case of the fishye-effect, everything outside of the reference shape remains unaltered).

 A background grid can be transformed along with the shape, making it possible to visualize how the transformation deforms the plane itself.

This project has three targets:
1) fancy images,
2) easy to use,
3) nice code.

## Fancy Showcase
The code to create these images is contained in the function 'create_fancy_image' of 'demo.py'.
![fancy example image 1](examples/fancy_step_1.png)

![fancy example image 2](examples/fancy_step_2.png)

## Examples
Here are three simple examples. The red shape is the reference-shape that defines the shape of the warp, while the warped shape is plotted in black. The code to create these images is also contained in 'demo.py', see the function 'create_simple_examples'.

### Mirror the plane at the red circle:
In this transformation, the black shaped is projected to the other side of the red shape, along the ray that runs through the center point at (0,0).
![mirror](examples/example_mirror.png)
### Construct a fisheye-effect inside the red circle:
Here, everything at the center of the red shape gets stretched outward, while everything near the inner boundary of the red shape gets squished. Outside of the red shape the image remains unaltered.
![fisheye](examples/example_fisheye.png)
### Project the full R²-plane into the inside of the blossom-shape defined by the red outline:
The final transformation maps the whole R²-plane into the red shape. The further away from the center, the more the space gets squished, and infinity is mapped to the outline of the red shape. Since the red shape is not a circle, the amount of how much a specific area gets squished depends on where the area is positioned with respect to the red shape.
![mirror](examples/example_subspace.png)

## Quick start
At first, we want to define a shape.
To define a shape, use a ShapeConstructor
```
from Shapes import ShapeConstructor
sc = ShapeConstructor()
```
and then create a shape-object, for example using one of the predefined distance-functions (these are functions f:(0,2\*pi)->R that map radians to angles, thus defining the outline of a shape in polar coordinates). For example, a windrose:
```
import DistanceFunctions as DF
windrose = sc.construct_from_distancefct(DF.distfct_windrose, name="windrose")
```
You don't have to specify a name, but the name of the shape can be used for plot titles.
For other possible shapes, see `DistanceFunctions.py`, where these functions are defined.
Note that you can also specify a shape by a list of points, this is supported by the functions `construct_from_points_cartesian` and `construct_from_points_polar` (depending on whether your points are in cartesian or in polar coordinates) of `ShapeConstructor`.

Now to transform our windrose-shape into something fancy, we need to choose a transformation and a second shape to specify the scope of the transformation.
Let's implement a fisheye-effect on the interior of a square.
Therefore we need a square-shape:
```
square = sc.construct_from_distancefct(DF.distfct_square, name="square")
```
And now, applying the transformation is straightforward, since the transformations are implemented as operators of shapes:
```
fancy_fisheye_windrose = windrose*square
```
By the way, the three currently implemented operators are:
- `shape|reference` implements the mirror-transformation,
- `shape*reference` implements the fisheye-effect,
- `shape**reference` implements the projection of R² into the reference shape.

Now all that's left is to plot our transformed shape.
To this end, we only need to initialize a matplotlib-figure and get the axes-element.
Since we want to plot a fancy image and not a mathematical function, we deactivate the axis and enforce that both dimensions have equal aspect:
```
from matplotlib import pyplot as plt
ax = plt.gca()
ax.set_aspect("equal")
ax.axis("off")
```
With this, we can simply tell our shape to go plot itself:
```
fancy_fisheye_windrose.plot(ax)
plt.show()
```

If you also want to display the reference-shape (the square) in red, as in the examples above, simply add the following line before the final `plt.show()`:
```
square.plot(ax, color='red', add_title=False, plot_background_grid=False)
```
Here, we explicitly state that the square should not overwrite the title of the plot (which was set to the name of the `fance_fisheye_windrose`-shape), and we also don't want the square to plot its background-grid.

![quickstart](examples/quickstart.png)

Oh, and this is what happens when you instead use the square as base shape and the windrose as reference for the fisheye-transformation (i.e. `fancy_fisheye_windrose = square*windrose`, and use the windrose-shape for the red plot in the end instead of the square):

![alternate quickstart](examples/quickstart_alternate.png)

## Requirements:
Python 3.x (any reasonably recent version should do) with
- numpy
- matplotlib

## Project structure:
- `Shapes.py`: the main classes that handle shapes, shape construction and shape transformations
- `Transformations.py`: implementations of the spacial transformations.
- `DistanceFunctions.py`: implementations of functions that define shape-geometry.
- `demo.py`: examples, mainly all the code required to reconstruct the examples from this presentation.
- `examples/`: generated example images

## Possible future extensions:
- More default shapes.
- More transformations.
- A minimal web interface where users could create parameterized shapes and transformations without needing to code.
- Extend the idea to full images.
