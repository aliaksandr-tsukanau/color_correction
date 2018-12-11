#  Copyright (c) 2018 Aliaksandr Tsukanau.
#  Licensed under GNU General Public Licence, version 3.
#  You may not use this file except in compliance with GNU General Public License, version 3.
#  See the GNU General Public License, version 3 for more details. https://www.gnu.org/licenses/gpl-3.0.en.html
#

from skimage import color
import matplotlib.pyplot as plt
import numpy as np
import pickle

from grid.grid import Grid


class Palette:
    def __init__(self, grid):
        self.lab = Palette._generate_lab_palette()
        self.mapping = self._load_or_create_mapping(grid)
        self.lab = np.moveaxis(self.lab, 0, 1)
        self.rgb = self._convert_lab_to_rgb()
        print(self.mapping)

    def _load_or_create_mapping(self, grid):
        try:
            with open('mapping.dat', 'rb') as f:
                mapping = pickle.load(file=f)
            return mapping
        except FileNotFoundError:
            mapping = np.apply_along_axis(self._get_nearest_index, 2, self.lab, grid)
            with open('mapping.dat', 'wb') as f:
                pickle.dump(mapping, file=f)
            return mapping

    @staticmethod
    def _generate_lab_palette(l_component=50):
        """generates square image as np array of shape (256, 256, 3)\
        in CIELAB color space where a and b vary from -127 to 128 along orthogonal directions of image\
        and L stays the same along the image and is set via l_component parameter"""
        ab = np.mgrid[-127:129, -127:129]
        # 2-dim array of a and b CIELAB components
        # a and b take values in range [-127; 128] sequentially

        l_ = np.full((256, 256), l_component)
        lab = np.empty((3, 256, 256))
        lab[0, :, :] = l_  # copying l component to result
        lab[1, :, :] = ab[0, :, :]  # copying a component to result
        lab[2, :, :] = ab[1, :, :]  # copying b component to result
        lab = np.moveaxis(lab, 0, 2)  # change axes order so that shape is (... , ... , 3) needed for skimage
        return lab

    def _convert_lab_to_rgb(self):
        rgb = color.lab2rgb(self.lab)
        rgb *= 255  # lab2rgb returns floats in range [0; 1] but we need uint8 numbers in [0; 255] for PyQt QImage
        rgb = np.require(rgb, np.uint8, 'C')
        return rgb

    def _get_nearest_index(self, point: np.ndarray, grid: Grid):
        nds = grid.initial_invisible_nodes
        # point_l = point[0]
        point = point[1:]
        dist = nds - point[np.newaxis, np.newaxis, :]
        dist = dist[:, :, 0] ** 2 + dist[:, :, 1] ** 2
        index = np.unravel_index(dist.argmin(), nds.shape[:2])
        # result = np.empty((3,))
        # result[0] = point_l
        # result[1:] = grid.invisible_nodes[index]
        return index


if __name__ == '__main__':
    # quick test using matplotlib
    grid = Grid(branches_number=8, radius=250, invisible_branches=320, inv_nodes_per_branch=71)
    palette = Palette(grid)
    plt.imshow(palette.rgb)
    plt.show()
