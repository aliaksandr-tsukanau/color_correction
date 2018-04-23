import numpy as np
from skimage import data
import matplotlib.pyplot as plt

INITIAL_IMAGE = data.chelsea()
# plt.imshow(INITIAL_IMAGE)
# plt.show()

PROCESSED_IMAGE = []  # np array 3 dim

LOOKUP_TABLE = []  #