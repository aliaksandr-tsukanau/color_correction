import numpy as np
import matplotlib.pyplot as plt
from math import degrees, atan2, radians, tan
from grid.grid_instance import grid

ab = np.array([[2, -6], [-40, 20]])



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

    bisector_angle = (theta1 + theta2) / 2
    # angle of bisector between i-th and (i+1) branches

    bisector_k = tan(radians(bisector_angle))
    # coefficient of bisector line equation so that the equation is:
    # b = bisector_k * a

    norm_k = 1 / -bisector_k
    norm_b = a0 / -bisector_k + b0
    # computed using analytical geometry formula for norm to a given line (bisector) through a given point (a0, b0)

    # Now we need to get intersections of norm with branches
    # b and h can be easily computed then

    line = [(a, norm_k*a) + norm_b for a in range(-20, 20)]
    plt.plot([p[0] for p in line], [p[1] for p in line])

    return norm_k, norm_b


print(np.apply_along_axis(_ab_to_dh, 0, ab))

plt.scatter(*ab)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
