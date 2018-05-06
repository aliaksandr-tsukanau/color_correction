from image.image import INITIAL_IMAGE, INITIAL_IMAGE_LAB, PROCESSED_IMAGE
import numpy as np
from skimage import color
from grid.grid_instance import grid
from math import atan2, degrees, tan, radians, sqrt, cos, sin
from color.transformations import ab_to_dhi, dhi_to_ab


def get_unique_colors_lab(image):
    """"""
    rgb_unique = np.unique(image.reshape(-1, image.shape[2]), axis=0)
    # rgb_unique = np.unique(np.ravel(image), axis=0)
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


def generate_initial_dhi(lut_ab_initial):
    return np.apply_along_axis(ab_to_dhi, 1, lut_ab_initial)
LUT_AB = {'initial': AB_UNIQUE, 'corrected': AB_UNIQUE}
# LUT_RGB = np.empty()

# LUT_DHI = {k: generate_initial_dhi(LUT_AB['initial']) for k in ['initial', 'corrected']}
# print(LUT_DHI['corrected'].shape)
#
# LUT_AB['corrected'] = np.apply_along_axis(dhi_to_ab, 1, LUT_DHI['corrected'])
# print(LUT_AB['corrected'].shape)
# print(LUT_AB)


def update_lut_ab(initial, grid):
    """calculates new colors mapped to initial colors using nodes positions"""

    raise NotImplementedError


def get_corrected_image():
    def change_lab_pixel(lab):
        l, b, a = lab
        new_pixel = np.empty((3,))
        new_pixel[0] = l
        i = np.where((LUT_AB['initial'] == (b, a)).all(axis=1))
        new_pixel[1:] = LUT_AB['corrected'][i]
        return new_pixel

    return np.apply_along_axis(change_lab_pixel, 2, INITIAL_IMAGE_LAB)


