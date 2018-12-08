from .node import Node


class Branch:
    """A collection of nodes which are by default located on the same line from center to periphery"""
    def __init__(self, angle, number_of_nodes, radius):
        self.radius = radius

        self.nodes = [
            Node.from_polar(
                r=self.radius * i / (number_of_nodes - 1),
                theta=angle,
                offset=self.radius
            )
            for i in range(0, number_of_nodes)
        ]

        # pin central and edge nodes
        for i in (0, -1):
            self.nodes[i].is_pinned = True

    def recalculate_child_nodes(self):
        nodes = self.nodes
        pinned_indices = [i for i, node in enumerate(nodes) if node.is_pinned]
        for prev, next_ in zip(pinned_indices, pinned_indices[1:]):
            # prev and next_ are indices of pinned nodes which hold all j-th nodes below in between
            for j in range(prev + 1, next_):
                nodes[j].x = nodes[prev].x + (nodes[next_].x - nodes[prev].x) * (j - prev) / (next_ - prev)
                nodes[j].y = nodes[prev].y + (nodes[next_].y - nodes[prev].y) * (j - prev) / (next_ - prev)

    def __repr__(self):
        return 'Branch(nodes_number=%d, radius=%r)' % (len(self.nodes), self.radius)
