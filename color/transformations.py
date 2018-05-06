import numpy as np
from math import degrees, atan2, radians, tan, sqrt, sin, cos, pi
from grid.grid_instance import grid


def ab_to_dhi(ab):
    """applies ab to dhi transformation to just one (a, b) pair"""
    # not divided into inner functions for computational efficiency

    a0, b0 = ab  # cartesian coordinates of given point in AB space

    # handle situation when a or b is 0
    if a0 == 0:
        d = np.abs(b0)
        i = 0 if d >= 0 else len(grid.branches) / 2
        return d, 0, i
    if b0 == 0:
        d = np.abs(a0)
        i = len(grid.branches) / 4 if d >= 0 else len(grid.branches) / 4 * 3
        return d, 0, i

    theta0 = (np.arctan2(b0, a0) + 2 * pi) % (2 * pi)  # angle which is a polar coordinate of given point
    branches_angles = np.array([radians(branch.angle) for branch in grid.branches])

    i = branches_angles[branches_angles < theta0].argmax()
    # index of branch with theta1
    # so point (a0, b0) is between i-th and (i+1)-th branches
    # and theta1 <= theta0 < theta2 (see below)

    theta1, theta2 = branches_angles[i],\
                     branches_angles[(i + 1) % branches_angles.shape[0]]
    # angles of branches that hold the point (a0, b0) in between

    bisector_angle = (theta1 + theta2) / 2
    # angle of bisector between i-th and (i+1) branches

    bisector_k = tan(bisector_angle)
    # coefficient of bisector line equation so that the equation is:
    # b = bisector_k * a

    def get_norm():
        norm_k = 1 / -bisector_k
        norm_b = a0 / bisector_k + b0
        return norm_k, norm_b

    norm_k, norm_b = get_norm()
    # norm to bisector through a given point (a0, b0)

    def get_intersection(branch_angle):
        """returns (a, b) coordinates of branch-norm intersection"""
        k = tan(branch_angle)
        intersection_a = norm_b / (k - norm_k)
        intersection_b = k * intersection_a
        return np.array([intersection_a, intersection_b])

    intersection1 = get_intersection(theta1)  # intersection with i-th branch

    def get_distance(point1: np.ndarray, point2: np.ndarray):
        dist = (point1 - point2) ** 2
        return sqrt(np.sum(dist))

    h = get_distance(ab, intersection1)
    d = get_distance(ab, np.zeros(2))
    return d, h, i


def dhi_to_ab(dhi: np.ndarray):
    """applies dhi to ab transformation to just one (d, h, i) tuple"""
    d, h, i = dhi
    angle_i = radians(grid.branches[int(i)].angle)
    ab_onbranch_i = d * cos(angle_i), d * sin(angle_i)
    # (a, b) coordinates of point on branch i at distance d from center

    angle_next = radians(grid.branches[int((i + 1) % len(grid.branches))].angle)
    ab_on_nextbranch = d * cos(angle_next), d * sin(angle_next)
    # (a, b) coordinates of point on branch next after the i-th at distance d from center

    diff = (ab_on_nextbranch[0] - ab_onbranch_i[0],
            ab_on_nextbranch[1] - ab_onbranch_i[1])
    h_direction = atan2(diff[1], diff[0])
    # angle between a axis and horde

    a = ab_onbranch_i[0] + h * cos(h_direction)
    b = ab_onbranch_i[1] + h * sin(h_direction)
    return a, b

#
# ab = np.array([[100, 99]])
#
# dhi = np.apply_along_axis(_ab_to_dhi, 1, ab)
# print(dhi)
#
# ab2 = np.apply_along_axis(_dhi_to_ab, 1, dhi)
#
# print(ab2)
# # plt.scatter(*ab[0])
# plt.scatter(*ab2[0])
# plt.gca().set_aspect('equal', adjustable='box')
# plt.show()
