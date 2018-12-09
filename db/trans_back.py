from grid.node import Node
from grid.branch import Branch
from grid.grid import Grid


def _dict_to_node(node_as_dict):
    def get_attrs(*attrs):
        for a in attrs:
            yield node_as_dict[a]

    init_x, init_y, x, y, offset, is_pinned = get_attrs('initial_x', 'initial_y', 'x', 'y', 'offset', 'is_pinned')
    node = Node(init_x, init_y, offset, is_pinned)
    node.x = x
    node.y = y
    return node


def _dict_to_branch(branch_as_dict):
    nodes = [_dict_to_node(node) for node in branch_as_dict['nodes']]
    return Branch(nodes)


def dict_to_grid(grid_as_dict) -> Grid:
    grid = Grid(branches_number=8, radius=250, invisible_branches=320, inv_nodes_per_branch=71)
    grid.branches = [_dict_to_branch(br) for br in grid_as_dict['branches']]
    grid.recalculate_invisibles()
    return grid
