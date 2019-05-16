#  Copyright (c) 2019 Aliaksandr Tsukanau.
#  Licensed under GNU General Public Licence, version 3.
#  You may not use this file except in compliance with GNU General Public License, version 3.
#  See the GNU General Public License, version 3 for more details. https://www.gnu.org/licenses/gpl-3.0.en.html
#
#

import numpy as np
from skimage import io, color


def read_initial_rgb(path='/home/sasha/Downloads/Telegram Desktop/photo_2019-05-16_17-47-12.jpg'):
    return io.imread(path)


def initial_to_lab(initial_rgb):
    return np.require(color.rgb2lab(initial_rgb), dtype='int8')


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


def get_unique_colors_for_pyqt(initial_rgb, radius):
    return get_unique_colors_lab(initial_rgb) / 128 * radius + radius

# contains unique colors for image uploaded to application
# as np array of shape (..., 2) containing pairs of (b, a) color coordinates in CIELAB color space


# TODO: switch to opencv for better speed
def process_img_with_lut(initial_lab, palette, grid, for_pyqt=True):
    # chain the two maps
    chained = grid.invisible_nodes[(*np.moveaxis(palette.mapping, 2, 0),)]
    # split color channels
    c1, *c23 = np.moveaxis(initial_lab, 2, 0)
    # add 128
    c23 = *map(np.add, c23, (127, 127)),
    # apply chained map
    processed_image_lab = np.concatenate([c1[..., None], chained[c23]], axis=2)
    processed_image_rgb = color.lab2rgb(processed_image_lab)
    if for_pyqt:
        processed_image_rgb = np.require(processed_image_rgb * 255, np.uint8, 'C')
    return processed_image_rgb


def save_processed_image(image, path):
    io.imsave(path, image)
