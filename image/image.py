import numpy as np
from skimage import data, io
import matplotlib.pyplot as plt

#INITIAL_IMAGE = io.imread('/home/sasha/Desktop/green_bubbles-wide.jpg')
INITIAL_IMAGE = data.hubble_deep_field()
# plt.imshow(INITIAL_IMAGE)
# plt.show()horse()

PROCESSED_IMAGE = []  # np array 3 dim

LOOKUP_TABLE = []  #