from .branch import Branch
from itertools import islice


class Grid:
    """For entire grid in GUI"""
    def __init__(self, branches_number, radius):
        # branches_number is also a number of node in a branch
        self.branches = [Branch(angle, nodes_number=branches_number, radius=radius)
                         for angle in range(0, 360, int(360 / branches_number))]
        self.radius = radius  # is needed for size of widget in GUI

    def nodes(self):
        """Generator that can be used to get all nodes of grid sequentially by branches.
        Left as method not property to distinguish from Branch.nodes field"""
        for branch in self.branches:
            for node in branch.nodes:
                yield node

    def __getitem__(self, item):
        return next(islice(self.nodes(), item))


    def __setitem__(self, key, value):
        self.branches[key // len(self.branches)].nodes[key % len(self.branches)] = value

