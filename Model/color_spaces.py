import numpy as np
import pprint
from skimage import color
import matplotlib.pyplot as plt


def _generate_lab_background(l_component=50):
    ab = np.mgrid[-127:129, -127:129]
    # 2-dim array of a and b CIELAB components
    # a and b take values in range [-127; 128] sequentially

    l = np.full((256, 256), l_component)
    lab = np.empty((3, 256, 256))
    lab[0, :, :] = l  # copying l component to result
    lab[1, :, :] = ab[0, :, :]  # copying a component to result
    lab[2, :, :] = ab[1, :, :]  # copying b component to result
    lab = np.moveaxis(lab, 0, 2)  # change axis order so that shape is (3, ... , ...) needed for skimage
    return lab


def _convert_lab_to_rgb():
    rgb = color.lab2rgb(LAB_BACKGROUND)
    rgb = rgb * 255
    rgb = np.require(rgb, np.uint8, 'C')
    return rgb


LAB_BACKGROUND = _generate_lab_background()
RGB_BACKGROUND = _convert_lab_to_rgb()

if __name__ == '__main__':
    plt.imshow(RGB_BACKGROUND)
    plt.show()

