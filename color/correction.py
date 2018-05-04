from image.image import INITIAL_IMAGE
import numpy as np
from skimage import color
from grid.grid_instance import grid
from math import atan2, degrees, tan, radians, sqrt, cos, sin


def get_unique_colors_lab(image):
    """"""
    rgb_unique = np.unique(image.reshape(-1, image.shape[2]), axis=0)
    rgb_unique = rgb_unique.reshape(rgb_unique.shape[0], 1, 3)
    # np array of shape (unique colors number, 1, 3) of unique (r, g, b) combinations without information of location
    # can be treated as image of height 1

    lab_unique = color.rgb2lab(rgb_unique)
    # same as rgb_unique but in CIELAB color space

    lab_unique_squeezed = np.squeeze(lab_unique)[:, 1:]

    return lab_unique_squeezed


def _ab_to_dhi(ab):
    """applies ab to dhi transformation to just one (a, b) pair"""

    a0, b0 = ab  # cartesian coordinates of given point in AB space

    # handle situation when a or b is 0
    if a0 == 0:
        d = abs(b0)
        i = 0 if d >= 0 else len(grid.branches) / 2
        return d, 0, i
    if b0 == 0:
        d = abs(a0)
        i = 0 if d >= 0 else len(grid.branches) / 2
        return d, 0, i

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

    def get_intersection(branch_angle):
        """returns (a, b) coordinates of branch-norm intersection"""
        k = tan(radians(branch_angle))
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


def generate_initial_dhi(lut_ab_initial):
    return np.apply_along_axis(_ab_to_dhi, 1, lut_ab_initial)


AB_UNIQUE = get_unique_colors_lab(INITIAL_IMAGE)

AB_UNIQUE_FOR_PYQT = AB_UNIQUE / 128 * grid.radius + grid.radius
# contains unique colors for image uploaded to application
# as np array of shape (..., 2) containing pairs of (b, a) color coordinates in CIELAB color space

LUT_AB = {'initial': AB_UNIQUE, 'corrected': AB_UNIQUE}
# LUT_RGB = np.empty()

LUT_DHI = {k: generate_initial_dhi(LUT_AB['initial']) for k in ['initial', 'corrected']}


def update_lut_ab(initial, grid):
    """calculates new colors mapped to initial colors using nodes positions"""

    raise NotImplementedError


def _dhi_to_ab(dhi: np.ndarray):
    """applies dhi to ab transformation to just one (d, h, i) tuple"""
    d, h, i = dhi
    angle_i = radians(grid.branches[i].angle)
    ab_onbranch_i = cos(angle_i), sin(angle_i)
    # (a, b) coordinates of point on branch i at distance d from center

    angle_next = radians(grid.branches[(i + 1) % len(grid.branches)].angle)
    ab_on_nextbranch = cos(angle_next), sin(angle_next)
    # (a, b) coordinates of point on branch next after the i-th at distance d from center

    diff = (ab_on_nextbranch[0] - ab_onbranch_i[0],
            ab_on_nextbranch[1] - ab_onbranch_i[1])
    h_direction = atan2(diff[1], diff[0])
    # angle between a axis and horde

    a = ab_onbranch_i + h * cos(h_direction)
    b = ab_onbranch_i + h * sin(h_direction)
    return a, b
