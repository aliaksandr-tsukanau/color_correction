import numpy as np
from skimage import data, io, color
import matplotlib.pyplot as plt

# from color.palette import PALETTE


# INITIAL_IMAGE = io.imread(r'C:\Users\aliaksandr.tsukanau\Desktop\sun.jpg')
# INITIAL_IMAGE = PALETTE.rgb
INITIAL_IMAGE = data.hubble_deep_field()
INITIAL_IMAGE_LAB = np.require(color.rgb2lab(INITIAL_IMAGE), dtype='int8')
# plt.imshow(INITIAL_IMAGE)
# plt.show()horse()

PROCESSED_IMAGE = []  # np array 3 dim

LOOKUP_TABLE = []  #