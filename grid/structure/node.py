from math import cos, sin, radians


class Node:
    """For a node in GUI grid"""
    def __init__(self, x, y, parent_branch: 'grid.structure.branch.Branch'):
        self.x = x
        self.y = y
        self._parent_branch = parent_branch  # is needed for conversion in coords_for_canvas
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
        offset = self._parent_branch.radius
        return self.x + offset, self.y + offset

    def __repr__(self):
        return 'Node(%r, %r, %s)' % (self.x, self.y, self.is_pinned)