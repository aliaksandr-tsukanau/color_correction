#  Copyright (c) 2018 Aliaksandr Tsukanau.
#  Licensed under GNU General Public Licence, version 3.
#  You may not use this file except in compliance with GNU General Public License, version 3.
#  See the GNU General Public License, version 3 for more details. https://www.gnu.org/licenses/gpl-3.0.en.html
#


import datetime as dt
import os
import skimage.io
from hashlib import sha256

from flask import Blueprint, request, jsonify, send_from_directory

from grid.grid import Grid
from image.image import initial_to_lab, process_img_with_lut
from db.client_instance import DB_CLIENT
from color.palette import Palette


processing_requests = Blueprint('processing_requests', __name__)


@processing_requests.route('/send_image', methods=['POST'])
def send_image():
    img_files = request.files
    assert len(img_files) == 1
    img_file = img_files['file']
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


@processing_requests.route('/process_image', methods=['GET'])
def process_image():
    img_token = request.args['image_token']
    grid_name = request.args['grid_name']

    path = _get_abs_path(img_token)
    initial_rgb = skimage.io.imread(path)
    initial_lab = initial_to_lab(initial_rgb)

    grid = DB_CLIENT.get_grid_obj(grid_name)

    processed = process_img_with_lut(initial_lab, PALETTE, grid)

    directory = os.path.join(os.getcwd(), 'files')
    directory = os.path.join(directory, 'processed_images')

    output_path = os.path.join(directory, img_token + '.jpeg')

    skimage.io.imsave(output_path, processed)
    return send_from_directory(
        directory,
        img_token + '.jpeg'
    )
