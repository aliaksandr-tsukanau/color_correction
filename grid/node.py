#  Copyright (c) 2019 Aliaksandr Tsukanau.
#  Licensed under GNU General Public Licence, version 3.
#  You may not use this file except in compliance with GNU General Public License, version 3.
#  See the GNU General Public License, version 3 for more details. https://www.gnu.org/licenses/gpl-3.0.en.html
#
#

from math import cos, sin, radians
import numpy as np


class Node:
    """For a node in GUI grid"""
    def __init__(self, x, y, offset, is_pinned=False):
        self.x = x
        self.initial_x = x
        self.y = y
        self.initial_y = y

        self.offset = offset

        self.is_pinned = is_pinned

    @classmethod
    def from_polar(cls, r, theta, offset, is_pinned=False):
        """(r, theta) are polar coordinates of node being created,
        whereas grid_radius stays for length of branch"""
        theta_radians = radians(theta)
        return cls(
            x=r * cos(theta_radians),
            y=r * sin(theta_radians),
            offset=offset,
            is_pinned=is_pinned,
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
