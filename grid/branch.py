#  Copyright (c) 2019 Aliaksandr Tsukanau.
#  Licensed under GNU General Public Licence, version 3.
#  You may not use this file except in compliance with GNU General Public License, version 3.
#  See the GNU General Public License, version 3 for more details. https://www.gnu.org/licenses/gpl-3.0.en.html
#
#

from typing import List

from attr import attrs

from .node import Node


@attrs(auto_attribs=True)
class Branch:
    """A collection of nodes which are by default located on the same line from center to periphery"""

    nodes: List[Node]

    @classmethod
    def from_angle(cls, angle, number_of_nodes, radius):
        last_idx = number_of_nodes - 1
        nodes = [
            Node.from_polar(
                r=radius * i / last_idx,
                theta=angle,
                offset=radius,
                is_pinned=(i == 0 or i == last_idx)  # pin central and edge nodes
            )
            for i in range(0, number_of_nodes)
        ]

        return cls(nodes)

    def recalculate_child_nodes(self):
        nodes = self.nodes
        pinned_indices = [i for i, node in enumerate(nodes) if node.is_pinned]
        for prev, next_ in zip(pinned_indices, pinned_indices[1:]):
            # prev and next_ are indices of pinned nodes which hold all j-th nodes below in between
            for j in range(prev + 1, next_):
                nodes[j].x = nodes[prev].x + (nodes[next_].x - nodes[prev].x) * (j - prev) / (next_ - prev)
                nodes[j].y = nodes[prev].y + (nodes[next_].y - nodes[prev].y) * (j - prev) / (next_ - prev)
