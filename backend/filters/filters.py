#  Copyright (c) 2019 Aliaksandr Tsukanau.
#  Licensed under GNU General Public Licence, version 3.
#  You may not use this file except in compliance with GNU General Public License, version 3.
#  See the GNU General Public License, version 3 for more details. https://www.gnu.org/licenses/gpl-3.0.en.html
#
#
import os

from flask.json import jsonify
from flask import Blueprint, request, send_from_directory

from backend.processing.processing import PALETTE
from db.client_instance import DB_CLIENT
from image.image import process_img_with_lut, read_initial_rgb, initial_to_lab, save_processed_image

filter_requests = Blueprint('filter_requests', __name__)


@filter_requests.route('/get_all_filters')
def all_filters():
    filter_names = DB_CLIENT.get_all_filter_names()
    return jsonify(filter_names)


@filter_requests.route('/get_filter_img_by_name')
def get_filter_img():
    orig_name = request.args['name']
    name = orig_name + '.jpeg'
    path = os.path.join(os.getcwd(), 'files')
    path = os.path.join(path, 'filter_icons')
    if os.path.exists(os.path.join(path, name)):
        return send_from_directory(
            path,
            name
        )
    else:
        grid = DB_CLIENT.get_grid_obj(orig_name)
        initial_path = os.path.join(os.getcwd(), 'files')
        initial_path = os.path.join(initial_path, 'filter_base.jpeg')
        initial = read_initial_rgb(initial_path)
        initial_lab = initial_to_lab(initial)
        icon = process_img_with_lut(initial_lab, PALETTE, grid, False)
        save_processed_image(icon, os.path.join(path, name))
        return send_from_directory(
            path,
            name
        )
