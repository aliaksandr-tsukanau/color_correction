from db.grid_driver import GridDatabaseDriver
from grid.grid import Grid

driver = GridDatabaseDriver()
grid = Grid(branches_number=8, radius=250, invisible_branches=320, inv_nodes_per_branch=71)

driver.save_grid(grid, 'testing_my_grid')

saved_grid = driver.get_grid('testing_my_grid')
