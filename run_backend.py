#  Copyright (c) 2018 Aliaksandr Tsukanau.
#  Licensed under GNU General Public Licence, version 3.
#  You may not use this file except in compliance with GNU General Public License, version 3.
#  See the GNU General Public License, version 3 for more details. https://www.gnu.org/licenses/gpl-3.0.en.html
#

import json
import bson.json_util

from flask import Flask, request, make_response
from flask.json import jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/color_correction'

mongo = PyMongo(app)


@app.route('/get_grid_by_name')
def root():
    name = request.args['name']
    grid = mongo.db.grids.find_one({'name': name})
    response_text = bson.json_util.dumps(grid)
    resp = make_response(response_text)
    resp.mimetype = 'application/json'
    return resp


@app.route('/get_all_filters')
def all_filters():
    grids = mongo.db.grids.find()
    json_content = bson.json_util.dumps(grids)
    filter_names = [grid['name'] for grid in json.loads(json_content)]
    return jsonify(filter_names)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
