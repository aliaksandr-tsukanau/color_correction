import numpy as np
from skimage import data, io
import matplotlib.pyplot as plt

from color.palette import RGB_BACKGROUND


# INITIAL_IMAGE = io.imread(r'C:\Users\aliaksandr.tsukanau\Desktop\sun.jpg')
# INITIAL_IMAGE = RGB_BACKGROUND
INITIAL_IMAGE = data.hubble_deep_field()
# plt.imshow(INITIAL_IMAGE)
# plt.show()horse()

PROCESSED_IMAGE = []  # np array 3 dim

LOOKUP_TABLE = []  #