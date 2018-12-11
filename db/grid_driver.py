#  Copyright (c) 2018 Aliaksandr Tsukanau.
#  Licensed under GNU General Public Licence, version 3.
#  You may not use this file except in compliance with GNU General Public License, version 3.
#  See the GNU General Public License, version 3 for more details. https://www.gnu.org/licenses/gpl-3.0.en.html
#

from pymongo import MongoClient

from db.trans_back import dict_to_grid
from db.transfrom import grid_to_dict
from grid.grid import Grid


class GridMongoClient:
    def __init__(self):
        self._client = MongoClient()
        self._db = self._client.color_correction

    def save_grid(self, grid: Grid, name):
        grid_as_dict = grid_to_dict(grid)
        self._db.grids.delete_many({
            'name': name
        })
        self._db.grids.insert({
            'name': name,
            'representation': grid_as_dict
        })

    def get_grid(self, name) -> Grid:
        grid_as_dict = self._db\
            .grids\
            .find_one({'name': name})
        representation = grid_as_dict['representation']
        return dict_to_grid(representation)

