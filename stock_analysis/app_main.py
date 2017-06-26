
# A very simple Flask Hello World app for you to get started with...

import flask
import json
from my_app import app
import server_io

@app.route('/json')
def json_world():
    return json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])

@app.route('/')
def hello_world():
    return "hallo from flask v" + str(flask.__version__)

if __name__ == '__main__':
      app.run(host='127.0.0.1', port=5001)
