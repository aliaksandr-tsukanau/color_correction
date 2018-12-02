from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/color_correction'

mongo = PyMongo(app)


@app.route('/')
def root():
    return 'Hello'


if __name__ == '__main__':
    app.run(debug=True)
