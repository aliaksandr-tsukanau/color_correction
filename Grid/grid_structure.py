from math import cos, sin, radians


class Node:
    """For a node in GUI grid"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_pinned = False

    @classmethod
    def from_polar(cls, r, theta):
        theta_radians = radians(theta)
        return cls(r * cos(theta_radians), r * sin(theta_radians))

    def __repr__(self):
        return 'Node(%r, %r, %s)' % (self.x, self.y, self.is_pinned)


class Branch:
    """A collection of nodes which are by default located on the same line from center to edge"""
    def __init__(self, angle, nodes_number, radius):
        self.nodes = [Node.from_polar(
                                      r=radius * i / (nodes_number - 1),
                                      theta=angle
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
