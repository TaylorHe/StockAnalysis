
# A very simple Flask Hello World app for you to get started with...
import sys
import flask
import json
from crossdomain import crossdomain

app = flask.Flask(__name__)

@app.route('/filein', methods=["POST"])
@crossdomain(origin="*")
def filein():
    try:
        data = json.loads(flask.request.data.decode(encoding="utf-8", errors="strict"))
        filename = data["name"]
        filename = "".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        handle = open("files/"+filename+".json","w")
        handle.write(json.dumps(data["file"]))
        handle.close()
        return json.dumps([True, "success"])
    except:
        return json.dumps([False, "internal error"])


@app.route('/fileout', methods=["POST"])
@crossdomain(origin="*")
def fileout():
    try:
        data = json.loads(flask.request.data.decode(encoding="utf-8", errors="strict"))
        filename = data["name"]
        filename = "".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        handle = None
        try:
            handle = open("files/"+filename+".json","r")
        except:
            handle = None
        if handle == None:
            return json.dumps([False, "file not found"])
        text = handle.read()
        handle.close()
        text.replace("\'", "'")
        # text = re.sub(r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'', text)
        text = json.loads(text)
        handle.close()
        return json.dumps([True, text])
    except:
        return json.dumps([False, "internal error"])

if __name__ == '__main__':
    #print(sys.argv)
    port = 4999
    if(len(sys.argv) == 2):
        port = int(sys.argv[1])
    app.run(host='127.0.0.1', port=port)
