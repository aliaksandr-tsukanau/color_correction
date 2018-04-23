from image.image import INITIAL_IMAGE
import numpy as np
from skimage import color
from grid.grid_instance import grid

RGB_UNIQUE = np.unique(INITIAL_IMAGE.reshape(-1, INITIAL_IMAGE.shape[2]), axis=0)
RGB_UNIQUE = RGB_UNIQUE.reshape(RGB_UNIQUE.shape[0], 1, 3)
LAB_UNIQUE = color.rgb2lab(RGB_UNIQUE)

AB_UNIQUE = np.squeeze(LAB_UNIQUE)[:, 1:]

AB_UNIQUE_FOR_PYQT = AB_UNIQUE / 128 * grid.radius + grid.radius
# contains unique colors for image uploaded to application
# as np array of shape (..., 2) containing pairs of (b, a) color coordinates in CIELAB color space




