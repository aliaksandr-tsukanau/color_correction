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


if __name__ == '__main__':
    app.run(debug=True)
