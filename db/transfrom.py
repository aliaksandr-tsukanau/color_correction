#  Copyright (c) 2019 Aliaksandr Tsukanau.
#  Licensed under GNU General Public Licence, version 3.
#  You may not use this file except in compliance with GNU General Public License, version 3.
#  See the GNU General Public License, version 3 for more details. https://www.gnu.org/licenses/gpl-3.0.en.html
#
#

import bson

from grid.branch import Branch
from grid.grid import Grid
from grid.node import Node


def _node_to_dict(node: Node):
    return {
        'x': float(node.x),
        'y': float(node.y),
        'initial_x': float(node.initial_x),
        'initial_y': float(node.initial_y),
        'offset': float(node.offset),
        'is_pinned': node.is_pinned,
    }


def _branch_to_dict(branch: Branch):
    return {
        'nodes': [_node_to_dict(node) for node in branch.nodes]
    }


def grid_to_dict(grid: Grid) -> dict:
    return {
        'radius': grid.radius,
        'branches': [_branch_to_dict(br) for br in grid.branches],
    }
