import numpy as np
from skimage import data, io, color
from grid.grid_instance import grid
from color.palette import PALETTE
from copy import deepcopy
import matplotlib.pyplot as plt

# from color.palette import PALETTE
from grid.grid_instance import grid


INITIAL_IMAGE = io.imread('/home/sasha/Downloads/Telegram Desktop/photo_2018-05-20_11-12-04.jpg')
# INITIAL_IMAGE = PALETTE.rgb
# INITIAL_IMAGE = data.astronaut()
INITIAL_IMAGE_LAB = np.require(color.rgb2lab(INITIAL_IMAGE), dtype='int8')
# plt.imshow(INITIAL_IMAGE)
# plt.show()horse()

PROCESSED_IMAGE = deepcopy(INITIAL_IMAGE)  # np array 3 dim


def get_unique_colors_lab(image):
    """"""
    rgb_unique = np.unique(image.reshape(-1, image.shape[2]), axis=0)
    # rgb_unique = np.unique(np.ravel(image), axis=0), (l, a, b)
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


def correct_image():
    # chain the two maps
    chained = grid.invisible_nodes[(*np.moveaxis(PALETTE.mapping, 2, 0),)]
    # split color channels
    c1, *c23 = np.moveaxis(INITIAL_IMAGE_LAB, 2, 0)
    # add 128
    c23 = *map(np.add, c23, (127, 127)),
    # apply chained map
    processed_image_lab = np.concatenate([c1[..., None], chained[c23]], axis=2)
    global PROCESSED_IMAGE
    PROCESSED_IMAGE = color.lab2rgb(processed_image_lab)
    plt.imshow(INITIAL_IMAGE)
    plt.imshow(PROCESSED_IMAGE)
    plt.show()
    PROCESSED_IMAGE = np.require(PROCESSED_IMAGE * 255, np.uint8, 'C')

