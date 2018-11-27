from math import cos, sin, radians
import numpy as np


class Node:
    """For a node in GUI grid"""
    def __init__(self, x, y, offset):
        self.x = x
        self.initial_x = x
        self.y = y
        self.initial_y = y

        self.offset = offset

        self.is_pinned = False

    @classmethod
    def from_polar(cls, r, theta, offset):
        """(r, theta) are polar coordinates of node being created,
        whereas grid_radius stays for length of branch"""
        theta_radians = radians(theta)
        return cls(
            x=r * cos(theta_radians),
            y=r * sin(theta_radians),
            offset=offset
        )

    @property
    def coords_for_canvas(self):
        return np.array([self.x, self.y]) + self.offset

    @property
    def numpy_coords(self):
        """returns self.x, self.y as numpy array"""
        return np.array([self.x, self.y])

    def __repr__(self):
        return 'Node(%r, %r, %s)' % (self.x, self.y, self.is_pinned)

    def move_to(self, new_x, new_y):
        """Updates nodes coordinates for entire branch stretching and squeezing regions between pinned nodes.
        new_x and new_y are coordinates in PyQt form (not zero-centered)"""
        self.is_pinned = True

        self.x = new_x
        self.y = new_y
