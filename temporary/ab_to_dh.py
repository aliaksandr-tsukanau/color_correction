import numpy as np
import matplotlib.pyplot as plt
from math import degrees, atan2, radians, tan
from grid.grid_instance import grid

ab = np.array([[2, 10, -9, 6], [40, 4, 7, -3]])
plt.scatter(*ab)
plt.show()


def _ab_to_dh(ab):
    """applies ab to dh transformation to just one (a, b) pair"""
    # not divided into inner functions for computational efficiency

    a0, b0 = ab  # cartesian coordinates of given point in AB space
    theta0 = (degrees(atan2(b0, a0)) + 360) % 360  # angle which is a polar coordinate of given point
    branches_angles = np.array([branch.angle for branch in grid.branches])

    i = branches_angles[branches_angles < theta0].argmax()
    # index of branch with theta1
    # so point (a0, b0) is between i-th and (i+1)-th branches
    # and theta1 <= theta0 < theta2 (see below)

    theta1, theta2 = branches_angles[i], branches_angles[(i + 1) % branches_angles.shape[0]]
    # angles of branches that hold the point (a0, b0) in between

    radial_angle = (theta1 + theta2) / 2
    radial_k = tan(radians(radial_angle))
    return radial_k


print(np.apply_along_axis(_ab_to_dh, 0, ab))
