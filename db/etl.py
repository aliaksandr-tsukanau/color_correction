from pymongo import MongoClient
from grid.grid import Grid
from grid.branch import Branch
from grid.node import Node


def _node_to_dict(node: Node):
    return vars(node)


def _branch_to_dict(branch: Branch):
    return {
        'nodes': [_node_to_dict(node) for node in branch.nodes]
    }


def grid_to_dict(grid: Grid) -> dict:
    return {
        'radius': grid.radius,
        'branches': [_branch_to_dict(br) for br in grid.branches],
    }


def dict_to_grid(grid_as_dict) -> Grid:
    raise NotImplementedError


class GridDB_Driver:
    def __init__(self):
        self._client = MongoClient()
        self._db = self._client.color_correction

    def save_grid(self, grid: Grid, name):
        grid_as_dict = grid_to_dict(grid)
        self._db.grids.insert({
            'name': name,
            'representation': grid_as_dict
        })

    def get_grid(self, name) -> Grid:
        grid_as_dict = self._db\
            .grids\
            .find_one({'name': name})\
            .representation
        return dict_to_grid(grid_as_dict)

