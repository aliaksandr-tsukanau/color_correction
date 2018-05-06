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

    def update_grid(self, new_x, new_y):
        """Updates nodes coordinates for entire branch stretching and squeezing regions between pinned nodes.
        new_x and new_y are coordinates in PyQt form (not zero-centered)"""
        self.is_pinned = True

        # convert to zero-centered
        offset = self.parent_branch.radius
        self.x = new_x - offset
        self.y = new_y - offset

        def recalculate_parent_branch(nodes: list):
            pinned_indices = [i for i, node in enumerate(nodes) if node.is_pinned]
            for prev, next_ in zip(pinned_indices, pinned_indices[1:]):
                # prev and next_ are indices of pinned nodes which hold all j-th nodes below in between
                for j in range(prev + 1, next_):
                    nodes[j].x = nodes[prev].x + (nodes[next_].x - nodes[prev].x) * (j - prev)/(next_ - prev)
                    nodes[j].y = nodes[prev].y + (nodes[next_].y - nodes[prev].y) * (j - prev) / (next_ - prev)

        def recalculate_invisibles(grid: 'grid.structure.Grid'):
            branch_indices = [i for i in range(0,
                                               grid.invisible_branches,
                                               int(grid.invisible_branches / len(grid.branches)))]
            node_indices = [j for j in range(0,
                                             grid.inv_nodes_per_branch,
                                             int(grid.inv_nodes_per_branch / (len(grid.branches) - 1)))]

            def recalculate_onbranches():
                for i, inv_i in enumerate(branch_indices):
                    for j, (inv_j_prev, inv_j_next) in enumerate(zip(node_indices, node_indices[1:])):
                        prev_node = grid.branches[i].nodes[j].numpy_coords
                        next_node = grid.branches[i].nodes[j + 1].numpy_coords
                        for k in range(inv_j_prev, inv_j_next + 1):
                            grid.invisible_nodes[inv_i, k] =\
                                    prev_node + (next_node - prev_node) / (inv_j_next - inv_j_prev) * (k - inv_j_prev)

            def recalculate_between():
                for j in range(grid.inv_nodes_per_branch):
                    for i, (inv_i_prev, inv_i_next) in \
                            enumerate(zip(branch_indices, branch_indices[1:] + [branch_indices[0]])):
                        prev_node = grid.invisible_nodes[inv_i_prev, j]
                        next_node = grid.invisible_nodes[inv_i_next, j]
                        for k in range(inv_i_prev, inv_i_next + 1):
                            grid.invisible_nodes[k, j] =\
                                    prev_node + (next_node - prev_node) / (inv_i_next - inv_i_prev) * (k - inv_i_prev)

            recalculate_onbranches()
            recalculate_between()

        recalculate_parent_branch(self.parent_branch.nodes)
        recalculate_invisibles(self.parent_branch.parent_grid)

    @property
    def displacement(self):
        """returns vector from initial to current coordinates as numpy array"""
        return np.array([self.x, self.y]) - self.initial_x

    def __repr__(self):
        return 'Node(%r, %r, %s)' % (self.x, self.y, self.is_pinned)
