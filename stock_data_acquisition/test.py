import requests
import json


r = requests.get('http://127.0.0.1:5002/requestStocks?start=2017-4-1&end=2017-5-1&stock=AAPL')
print(r.text)

#r = requests.post('http://127.0.0.1:' + str(port) + '/fileout', data = json.dumps({"name":"tweets"}))
#print(r.text)
#print(json.loads(r.text))
