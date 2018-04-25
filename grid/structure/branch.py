from .node import Node


class Branch:
    """A collection of nodes which are by default located on the same line from center to edge"""
    def __init__(self, angle, nodes_number, radius):
        self.nodes = [Node.from_polar(
                                      r=radius * i / (nodes_number - 1),
                                      theta=angle,
                                      parent_branch=self
                                     )
                      for i in range(0, nodes_number)]

        # pin central and edge nodes
        for i in (0, -1):
            self.nodes[i].is_pinned = True

        self.angle = angle
        self.radius = radius

    def __repr__(self):
        return 'Branch(angle=%r, nodes_number=%d, radius=%r)' % (self.angle, len(self.nodes), self.radius)
