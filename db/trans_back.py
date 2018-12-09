from grid.branch import Branch
from grid.grid import Grid


def _dict_to_node(node_as_dict):
    pass


def _dict_to_branch(branch_as_dict):
    pass


def dict_to_grid(grid_as_dict) -> Grid:
    grid = Grid(branches_number=8, radius=250, invisible_branches=320, inv_nodes_per_branch=71)
    grid.branches = [_dict_to_branch(br) for br in grid_as_dict['branches']]
    grid.recalculate_invisibles()
    return grid
