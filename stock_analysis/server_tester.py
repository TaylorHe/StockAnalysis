
# A very simple Flask Hello World app for you to get started with...

import flask
import json
from crossdomain import crossdomain

app = flask.Flask(__name__)

@app.route('/json', methods=["POST","GET"])
@crossdomain(origin="*")
def json_world():
    return json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])

@app.route('/senditback', methods=["POST","GET"])
@crossdomain(origin="*")
def json_bounce():
    data = json.loads(flask.request.data.decode("utf-8"))
    print(data)
    return json.dumps(data)

@app.route('/')
def hello_world():
    return "hallo from flask v" + str(flask.__version__)

@app.route('/file')
def file_upload():
    r = requests.post('http://httpbin.org/post', data = {'key':'value'})


if __name__ == '__main__':
      app.run(host='127.0.0.1', port=4999)
