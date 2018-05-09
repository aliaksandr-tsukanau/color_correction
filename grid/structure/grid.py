from .branch import Branch
import numpy as np


class Grid:

    """For entire grid in GUI"""
    def __init__(self, branches_number, radius, invisible_branches, inv_nodes_per_branch):
        # branches_number is also a number of node in a branch
        # branches_number must be dividable by 4
        # invisible_branches and inv_nodes_per_branch must be chosen so that invisible nodes contain visible
        self.radius = radius  # is needed for size of widget in GUI
        self.branches = [Branch(angle, nodes_number=branches_number, grid=self)
                         for angle in range(0, 360, int(360 / branches_number))]
        self.invisible_nodes = self._init_invisible_nodes(invisible_branches, inv_nodes_per_branch, radius)
        self.initial_invisible_nodes = self.invisible_nodes
        self.invisible_branches = invisible_branches
        self.inv_nodes_per_branch = inv_nodes_per_branch

    def _init_invisible_nodes(self, inv_branches, inv_nodes_per_branch, radius):
        nodes = np.empty((inv_branches, inv_nodes_per_branch, 2))
        angle_between_br = 2 * np.pi / len(self.branches)
        shortest_inv_branch_radius = radius * np.cos(angle_between_br / 2)
        # argument of cos is half of angle between branches
        for i in range(inv_branches):
            for j in range(inv_nodes_per_branch):
                angle = np.pi * 2 / inv_branches * i
                current_inv_branch_radius =\
                    shortest_inv_branch_radius / np.cos(angle_between_br / 2 - angle % angle_between_br)
                r = current_inv_branch_radius / (inv_nodes_per_branch - 1) * j
                nodes[i, j, :] = r * np.cos(angle), r * np.sin(angle)
        return nodes

    def nodes(self):
        """Generator that can be used to get all nodes of grid sequentially by branches.
        Left as method not property to distinguish from Branch.nodes field"""
        for branch in self.branches:
            for node in branch.nodes:
                yield node

    def recalculate_invisibles(self):
        branch_indices = [i for i in range(0,
                                           self.invisible_branches,
                                           int(self.invisible_branches / len(self.branches)))]
        node_indices = [j for j in range(0,
                                         self.inv_nodes_per_branch,
                                         int(self.inv_nodes_per_branch / (len(self.branches) - 1)))]

        def recalculate_onbranches():
            for i, inv_i in enumerate(branch_indices):
                for j, (inv_j_prev, inv_j_next) in enumerate(zip(node_indices, node_indices[1:])):
                    prev_node = self.branches[i].nodes[j].numpy_coords
                    next_node = self.branches[i].nodes[j + 1].numpy_coords
                    for k in range(inv_j_prev, inv_j_next + 1):
                        self.invisible_nodes[inv_i, k] = \
                            prev_node + (next_node - prev_node) / (inv_j_next - inv_j_prev) * (k - inv_j_prev)

        def recalculate_between():
            for j in range(self.inv_nodes_per_branch):
                for i, (inv_i_prev, inv_i_next) in \
                        enumerate(zip(branch_indices, branch_indices[1:] + [branch_indices[0]])):
                    prev_node = self.invisible_nodes[inv_i_prev, j]
                    next_node = self.invisible_nodes[inv_i_next, j]
                    upper_bounder = inv_i_next if i != 7 else self.invisible_branches - 1
                    for k in range(inv_i_prev, upper_bounder + 1):
                        self.invisible_nodes[k, j] = prev_node \
                                + (next_node - prev_node) / (upper_bounder - inv_i_prev) * (k - inv_i_prev)

        recalculate_onbranches()
        recalculate_between()

    def __getitem__(self, item):
        return self.branches[item // len(self.branches)].nodes[item % len(self.branches)]

    def __setitem__(self, key, value):
        self.branches[key // len(self.branches)].nodes[key % len(self.branches)] = value
