#  Copyright (c) 2018 Aliaksandr Tsukanau.
#  Licensed under GNU General Public Licence, version 3.
#  You may not use this file except in compliance with GNU General Public License, version 3.
#  See the GNU General Public License, version 3 for more details. https://www.gnu.org/licenses/gpl-3.0.en.html
#

import bson.json_util

from flask import Flask, request, make_response
from flask.json import jsonify

from db.grid_driver import GridMongoClient

app = Flask(__name__)
db_client = GridMongoClient()


@app.route('/get_grid_by_name')
def root():
    name = request.args['name']
    grid = db_client.get_grid_bson(name)
    response_text = bson.json_util.dumps(grid)
    resp = make_response(response_text)
    resp.mimetype = 'application/json'
    return resp


@app.route('/get_all_filters')
def all_filters():
    filter_names = db_client.get_all_filter_names()
    return jsonify(filter_names)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
