#  Copyright (c) 2018 Aliaksandr Tsukanau.
#  Licensed under GNU General Public Licence, version 3.
#  You may not use this file except in compliance with GNU General Public License, version 3.
#  See the GNU General Public License, version 3 for more details. https://www.gnu.org/licenses/gpl-3.0.en.html
#

from db.grid_driver import GridMongoClient
from grid.grid import Grid

driver = GridMongoClient()
grid = Grid(branches_number=8, radius=250, invisible_branches=320, inv_nodes_per_branch=71)

driver.save_grid(grid, 'testing_my_grid')

saved_grid = driver.get_grid_obj('testing_my_grid')
