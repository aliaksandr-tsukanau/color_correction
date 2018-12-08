from db.etl import GridDB_Driver
from grid.grid import Grid

driver = GridDB_Driver()
grid = Grid(branches_number=8, radius=250, invisible_branches=320, inv_nodes_per_branch=71)

driver.save_grid(grid, 'testing_my_grid')
