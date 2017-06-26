import requests
import json
port = 5004


r = requests.post('http://127.0.0.1:' + str(port) + '/filein', data = json.dumps({"name":"pytest","file":{"sizeofarock":"very big"}}))
print(r.text)

r = requests.post('http://127.0.0.1:' + str(port) + '/fileout', data = json.dumps({"name":"tweets"}))
#print(r.text)
print(json.loads(r.text))
