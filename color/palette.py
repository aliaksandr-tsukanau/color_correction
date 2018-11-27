from skimage import color
import matplotlib.pyplot as plt
from grid.grid_instance import grid
import numpy as np
import pickle


class Palette:
    def __init__(self):
        self.lab = Palette._generate_lab_palette()
        self.rgb = self._convert_lab_to_rgb()
        self.mapping = self._load_or_create_mapping()
        print(self.mapping)

    def _load_or_create_mapping(self):
        try:
            with open('mapping.dat', 'rb') as f:
                mapping = pickle.load(file=f)
            return mapping
        except FileNotFoundError:
            mapping = np.apply_along_axis(self._get_nearest_index, 2, self.lab)
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
        lab = np.moveaxis(lab, 0, 1)
        return lab

    def _convert_lab_to_rgb(self):
        rgb = color.lab2rgb(self.lab)
        rgb *= 255  # lab2rgb returns floats in range [0; 1] but we need uint8 numbers in [0; 255] for PyQt QImage
        rgb = np.require(rgb, np.uint8, 'C')
        return rgb

    def _get_nearest_index(self, point: np.ndarray):
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


PALETTE = Palette()

if __name__ == '__main__':
    # quick test using matplotlib
    plt.imshow(PALETTE.rgb)
    plt.show()
