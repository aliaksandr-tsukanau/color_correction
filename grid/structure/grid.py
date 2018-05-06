from .branch import Branch
import numpy as np


class Grid:
    # class InvisibleNodes:
    #     def __init__(self, branches_number, radius, nodes_on_branch, nodes_on_edge):
    #         edges_number = branches_number
    #
    #         self.onbranch = np.empty((branches_number, nodes_on_branch, 2))
    #         # self.onbranch[branch_idx, idx_on_branch] = a, b
    #
    #         self.onedge = np.empty((branches_number, edges_number, nodes_on_edge, 2))
    #         # self.onedge[branch_idx, edge_idx, idx_on_edge] = a, b
    #
    #         self.intersections = np.empty((branches_number, nodes_on_branch, edges_number, nodes_on_edge))
    #         # self.intersections[branch_idx, idx_on_branch, edge_idx, idx_on_edge] = a, b

    """For entire grid in GUI"""
    def __init__(self, branches_number, radius, invisible_branches, inv_nodes_per_branch):
        # branches_number is also a number of node in a branch
        self.branches = [Branch(angle, nodes_number=branches_number, radius=radius)
                         for angle in range(0, 360, int(360 / branches_number))]
        self.radius = radius  # is needed for size of widget in GUI
        self.invisible_nodes = self._init_invisible_nodes(invisible_branches, inv_nodes_per_branch, radius)

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
                r = current_inv_branch_radius / inv_nodes_per_branch * j
                nodes[i, j, :] = r * np.cos(angle), r * np.sin(angle)
        return nodes

    def nodes(self):
        """Generator that can be used to get all nodes of grid sequentially by branches.
        Left as method not property to distinguish from Branch.nodes field"""
        for branch in self.branches:
            for node in branch.nodes:
                yield node

    def __getitem__(self, item):
        return self.branches[item // len(self.branches)].nodes[item % len(self.branches)]

    def __setitem__(self, key, value):
        self.branches[key // len(self.branches)].nodes[key % len(self.branches)] = value


