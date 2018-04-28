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

    def update_branch(self, new_x, new_y):
        """Updates nodes coordinates for entire branch stretching and squeezing regions between pinned nodes.
        new_x and new_y are coordinates in PyQt form (not zero-centered)"""
        self.is_pinned = True

        # convert to zero-centered
        offset = self._parent_branch.radius
        self.x = new_x - offset
        self.y = new_y - offset

        def _recalculate_parent_branch(nodes: list):
            pinned_indices = [i for i, node in enumerate(nodes) if node.is_pinned]
            for prev, next_ in zip(pinned_indices, pinned_indices[1:]):
                # prev and next_ are indices of pinned nodes which hold all j-th nodes below in between
                for j in range(prev + 1, next_):
                    nodes[j].x = nodes[prev].x + (nodes[next_].x - nodes[prev].x) * (j - prev)/(next_ - prev)
                    nodes[j].y = nodes[prev].y + (nodes[next_].y - nodes[prev].y) * (j - prev) / (next_ - prev)

        _recalculate_parent_branch(self._parent_branch.nodes)

    def __repr__(self):
        return 'Node(%r, %r, %s)' % (self.x, self.y, self.is_pinned)