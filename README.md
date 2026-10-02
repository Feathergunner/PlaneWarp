# Plane Warp
A small hobby project to construct interesting transformations of 2D-shapes.

## Fancy Showcase
![fancy example image 1](examples/fancy_step_1.png)

![fancy example image 2](examples/fancy_step_2.png)

## Examples
Here are three simple examples. The red shape is the reference-shape that defines the shape of the warp, while the warped shape is plotted in black.

### Mirror the plane at the red circle:
![mirror](examples/example_mirror.png)
### construct a fisheye-effect inside the red circle:
![fisheye](examples/example_fisheye.png)
### project the full R²-plane into the inside of the blossom-shape defined by the red outline:
![mirror](examples/example_subspace.png)

## How To
See 'demo.py' for a small demo that generates the images above.
The function 'create_simple_examples' generates the three simple examples.
The function 'create_fancy_image' generates the fancy images from the showcase at the top.

## Requirements:
- numpy
- matplotlib
