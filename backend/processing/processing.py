#  Copyright (c) 2019 Aliaksandr Tsukanau.
#  Licensed under GNU General Public Licence, version 3.
#  You may not use this file except in compliance with GNU General Public License, version 3.
#  See the GNU General Public License, version 3 for more details. https://www.gnu.org/licenses/gpl-3.0.en.html
#
#


import datetime as dt
import os
from functools import lru_cache

import skimage.io
from hashlib import sha256
from flask import Blueprint, request, jsonify, send_from_directory

from grid.grid import Grid
from image.image import initial_to_lab, process_img_with_lut
from db.client_instance import DB_CLIENT
from color.palette import Palette


processing_requests = Blueprint('processing_requests', __name__)


class InvalidImageFile(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@processing_requests.errorhandler(InvalidImageFile)
def handle_invalid_usage(error: InvalidImageFile):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


ALLOWED_EXTENSIONS = {'.jpeg', '.jpg'}


def _is_jpg(file):
    return any(
        file.filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS
    )


@processing_requests.route('/send_image', methods=['POST'])
def send_image():
    img_files = request.files
    if len(img_files) != 1:
        raise InvalidImageFile('Expected one image file, got a different number')
    img_file = img_files['file']
    if not _is_jpg(img_file):
        raise InvalidImageFile('File is not JPEG')
    rel_path = _get_img_token(img_file.filename)
    abs_path = _get_abs_path(rel_path)
    img_file.save(abs_path)
    return jsonify({'image_token': rel_path})


def _get_img_token(name: str):
    now = dt.datetime.utcnow()
    hash_ = sha256()
    hash_.update(str(now).encode('utf-8'))
    hash_.update(name.encode('utf-8'))
    rel_path = str(hash_.hexdigest())
    return rel_path


def _get_abs_path(rel_path):
    abs_path = os.getcwd()
    for part in ('files', 'initial_images', rel_path):
        abs_path = os.path.join(abs_path, part)
    abs_path += '.jpeg'
    return abs_path


def _get_palette():
    default_grid = Grid(branches_number=8, radius=250, invisible_branches=320, inv_nodes_per_branch=71)
    return Palette(default_grid)


PALETTE = _get_palette()


@lru_cache(maxsize=50)
def _cached_read_img_into_lab(path):
    initial_rgb = skimage.io.imread(path)
    return initial_to_lab(initial_rgb)


@lru_cache(maxsize=150)
def _cached_get_processed_img(image_token, grid_name):
    path = _get_abs_path(image_token)
    initial_lab = _cached_read_img_into_lab(path)

    grid = DB_CLIENT.get_grid_obj(grid_name)

    return process_img_with_lut(initial_lab, PALETTE, grid)


@processing_requests.route('/process_image', methods=['GET'])
def process_image():
    img_token = request.args['image_token']
    grid_name = request.args['grid_name']

    processed = _cached_get_processed_img(img_token, grid_name)

    directory = os.path.join(os.getcwd(), 'files')
    directory = os.path.join(directory, 'processed_images')

    output_path = f'{img_token}{grid_name}.jpeg'

    skimage.io.imsave(os.path.join(directory, output_path), processed)
    response = send_from_directory(
        directory,
        output_path,
    )
    return response

