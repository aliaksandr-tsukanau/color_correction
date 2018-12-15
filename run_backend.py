#  Copyright (c) 2018 Aliaksandr Tsukanau.
#  Licensed under GNU General Public Licence, version 3.
#  You may not use this file except in compliance with GNU General Public License, version 3.
#  See the GNU General Public License, version 3 for more details. https://www.gnu.org/licenses/gpl-3.0.en.html
#

import bson.json_util

from flask import Flask, request, make_response
from backend.filters import filter_requests

from db.client_instance import DB_CLIENT

app = Flask(__name__)
BLUPRINTS = [
    filter_requests,
]

for b in BLUPRINTS:
    app.register_blueprint(b)


@app.route('/get_grid_by_name')
def root():
    name = request.args['name']
    grid = DB_CLIENT.get_grid_bson(name)
    response_text = bson.json_util.dumps(grid)
    resp = make_response(response_text)
    resp.mimetype = 'application/json'
    return resp


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
