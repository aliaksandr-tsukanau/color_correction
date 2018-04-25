from image.image import INITIAL_IMAGE
import numpy as np
from skimage import color
from grid.grid_instance import grid
from math import atan2, degrees


def get_unique_colors_lab(image):
    """"""
    rgb_unique = np.unique(image.reshape(-1, image.shape[2]), axis=0)
    rgb_unique = rgb_unique.reshape(rgb_unique.shape[0], 1, 3)
    # np array of shape (unique colors number, 1, 3) of unique (r, g, b) combinations without information of location
    # can be treated as image of height 1

    lab_unique = color.rgb2lab(rgb_unique)
    # same as rgb_unique but in CIELAB color space

    lab_unique_squeezed = np.squeeze(lab_unique)[:, 1:]

    return lab_unique_squeezed


AB_UNIQUE = get_unique_colors_lab(INITIAL_IMAGE)

AB_UNIQUE_FOR_PYQT = AB_UNIQUE / 128 * grid.radius + grid.radius
# contains unique colors for image uploaded to application
# as np array of shape (..., 2) containing pairs of (b, a) color coordinates in CIELAB color space

LUT_AB = {'initial': AB_UNIQUE, 'corrected': AB_UNIQUE}
# LUT_RGB = np.empty()


def _ab_to_dh(ab):
    """applies ab to dh transformation to just one (a, b) pair"""
    # not divided into inner functions for computational efficiency

    a, b = ab[1], ab[0]
    theta = degrees(atan2(b, a))
    branches_angles = np.ndarray([branch.angle for branch in grid.branches])
    
    # theta -> theta1, theta2
    # avg(theta1, theta2) -> radial line equation at avg angle
    # line through (a, b) perpendicular to radial
    pass


def generate_initial_dh(lut_ab_initial):
    pass
    # np.apply_along_axis()


DH = {k: generate_initial_dh(LUT_AB['initial']) for k in ['initial', 'corrected']}


def update_lut_ab(initial, grid):
    """calculates new colors mapped to initial colors using nodes positions"""

    raise NotImplementedError


