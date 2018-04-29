import numpy as np
import matplotlib.pyplot as plt
from math import degrees, atan2, radians, tan, sqrt
from grid.grid_instance import grid


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

    def get_norm():
        norm_k = 1 / -bisector_k
        norm_b = a0 / bisector_k + b0
        return norm_k, norm_b

    norm_k, norm_b = get_norm()
    # norm to bisector through a given point (a0, b0)

    line = [(a, norm_k * a + norm_b) for a in range(-20, 20)]
    plt.plot([p[0] for p in line], [p[1] for p in line])

    # Now we need to get intersections of norm with branches
    def get_intersection(branch_angle):
        """returns (a, b) coordinates of branch-norm intersection"""
        k = tan(radians(branch_angle))
        intersection_a = norm_b / (k - norm_k)
        intersection_b = k * intersection_a
        return np.array([intersection_a, intersection_b])

    intersection1 = get_intersection(theta1)
    plt.scatter(*intersection1)

    intersection2 = get_intersection(theta2)
    plt.scatter(*intersection2)

    # b and h can be easily computed then

    def get_distance(point1: np.ndarray, point2: np.ndarray):
        d = (point1 - point2) ** 2
        return sqrt(d[0] + d[1])

    h = get_distance(ab, intersection1)
    d = get_distance(ab, np.zeros(2))
    return d, h


ab = np.array([[3], [6]])

print(np.apply_along_axis(_ab_to_dh, 0, ab))

plt.scatter(*ab)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
