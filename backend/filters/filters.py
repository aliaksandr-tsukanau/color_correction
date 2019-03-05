#  Copyright (c) 2019 Aliaksandr Tsukanau.
#  Licensed under GNU General Public Licence, version 3.
#  You may not use this file except in compliance with GNU General Public License, version 3.
#  See the GNU General Public License, version 3 for more details. https://www.gnu.org/licenses/gpl-3.0.en.html
#
#
import os

from flask.json import jsonify
from flask import Blueprint, request, send_from_directory

from db.client_instance import DB_CLIENT

filter_requests = Blueprint('filter_requests', __name__)


@filter_requests.route('/get_all_filters')
def all_filters():
    filter_names = DB_CLIENT.get_all_filter_names()
    return jsonify(filter_names)


@filter_requests.route('/get_filter_img_by_name')
def get_filter_img():
    name = request.args['name'] + '.jpeg'
    path = os.path.join(os.getcwd(), 'files')
    path = os.path.join(path, 'filter_icons')
    return send_from_directory(
        path,
        name
    )
