from math import cos, sin, radians


class Node:
    """For a node in GUI grid"""
    def __init__(self, x, y, grid_radius):
        self.x = x
        self.y = y
        self._grid_radius = grid_radius  # is needed for conversion in coords_for_canvas
        self.is_pinned = False

    @classmethod
    def from_polar(cls, r, theta, grid_radius):
        """(r, theta) are polar coordinates of node being created,\
        whereas grid_radius stays for length of branch"""
        theta_radians = radians(theta)
        return cls(x=r * cos(theta_radians),
                   y=r * sin(theta_radians),
                   grid_radius=grid_radius)

    @property
    def coords_for_canvas(self):
        """returns a tuple of node coordinates converted form zero-centered to PyQt's"""
        return self.x + self._grid_radius, self.y + self._grid_radius

    def __repr__(self):
        return 'Node(%r, %r, %s)' % (self.x, self.y, self.is_pinned)


class Branch:
    """A collection of nodes which are by default located on the same line from center to edge"""
    def __init__(self, angle, nodes_number, radius):
        self.nodes = [Node.from_polar(
                                      r=radius * i / (nodes_number - 1),
                                      theta=angle,
                                      grid_radius=radius
                                     )
                      for i in range(0, nodes_number)]

        # pin central and edge nodes
        for i in (0, -1):
            self.nodes[i].is_pinned = True

        self._angle = angle
        self._radius = radius

    def __repr__(self):
        return 'Branch(angle=%r, nodes_number=%d, radius=%r)' % (self._angle, len(self.nodes), self._radius)


class Grid:
    """For entire grid in GUI"""
    def __init__(self, branches_number, radius):
        # branches_number is also a number of node in a branch
        self.branches = [Branch(angle, nodes_number=branches_number, radius=radius)
                         for angle in range(0, 360, int(360 / branches_number))]
        self.radius = radius  # is needed for size of widget in GUI

    def nodes(self):
        """generator that can be used to get all nodes of grid sequentially by branches"""
        for branch in self.branches:
            for node in branch.nodes:
                yield node
