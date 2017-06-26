import requests
import json
from myurl import url, port

handle = open("data.json", "r")
data = json.loads(handle.read())
handle.close()

r = requests.post(url + ':' + port + '/filein', data = json.dumps({"name":"tweetweets","file":data}))
print(r.text)

