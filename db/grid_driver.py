#  Copyright (c) 2019 Aliaksandr Tsukanau.
#  Licensed under GNU General Public Licence, version 3.
#  You may not use this file except in compliance with GNU General Public License, version 3.
#  See the GNU General Public License, version 3 for more details. https://www.gnu.org/licenses/gpl-3.0.en.html
#
#
from functools import lru_cache

from pymongo import MongoClient

from db.trans_back import dict_to_grid
from db.transfrom import grid_to_dict
from grid.grid import Grid


class GridMongoClient:
    def __init__(self):
        self._client = MongoClient()
        self._db = self._client.color_correction
        self._grids = self._db.grids

    def save_grid(self, grid: Grid, name):
        grid_as_dict = grid_to_dict(grid)
        self._grids.delete_many({
            'name': name
        })
        self._grids.insert({
            'name': name,
            'representation': grid_as_dict
        })

    @lru_cache(maxsize=50)
    def get_grid_obj(self, name) -> Grid:
        grid_as_dict = self.get_grid_bson(name)
        representation = grid_as_dict['representation']
        return dict_to_grid(representation)

    def get_grid_bson(self, name) -> dict:
        return self._grids\
                   .find_one({'name': name})

    def get_all_filter_names(self) -> list:
        all_grids = self._grids.find()
        filter_names = [grid['name'] for grid in all_grids]
        return filter_names
