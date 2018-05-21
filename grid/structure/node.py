from math import cos, sin, radians
import numpy as np


class Node:
    """For a node in GUI grid"""
    def __init__(self, x, y, parent_branch: 'grid.structure.branch.Branch'):
        self.x = x
        self.initial_x = x
        self.y = y
        self.initial_y = y
        self.parent_branch = parent_branch  # is needed for conversion in coords_for_canvas
        self.is_pinned = False

    @classmethod
    def from_polar(cls, r, theta, parent_branch: 'grid.structure.branch.Branch'):
        """(r, theta) are polar coordinates of node being created,\
        whereas grid_radius stays for length of branch"""
        theta_radians = radians(theta)
        return cls(x=r * cos(theta_radians),
                   y=r * sin(theta_radians),
                   parent_branch=parent_branch)

    @property
    def coords_for_canvas(self):
        """returns a tuple of node coordinates converted form zero-centered to PyQt's"""
        offset = self.parent_branch.radius
        return self.x + offset, self.y + offset

    @property
    def numpy_coords(self):
        """returns self.x, self.y as numpy array"""
        return np.array([self.x, self.y])

    def update_grid(self, new_x, new_y, recalculate_all=False):
        """Updates nodes coordinates for entire branch stretching and squeezing regions between pinned nodes.
        new_x and new_y are coordinates in PyQt form (not zero-centered)"""
        self.is_pinned = True

        # convert to zero-centered
        offset = self.parent_branch.radius
        self.x = new_x - offset
        self.y = new_y - offset

        self.parent_branch.recalculate_child_nodes()
        if recalculate_all:
            self.parent_branch.parent_grid.recalculate_invisibles()

    @property
    def displacement(self):
        """returns vector from initial to current coordinates as numpy array"""
        return np.array([self.x, self.y]) - self.initial_x

    def __repr__(self):
        return 'Node(%r, %r, %s)' % (self.x, self.y, self.is_pinned)
