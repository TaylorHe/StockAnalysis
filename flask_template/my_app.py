
# A very simple Flask Hello World app for you to get started with...

import sys
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
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

if __name__ == '__main__':
    #print(sys.argv)
    port = 4999
    if(len(sys.argv) == 2):
        port = int(sys.argv[1])
    app.run(host='127.0.0.1', port=port)
