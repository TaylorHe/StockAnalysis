import flask
from crossdomain import crossdomain
import json
import datetime
from my_app import app
import requests

IS_LIVE = False
CAN_WRITE = True
try:
    IS_LIVE = input("Run in LiveMode? y/n (Requires the standard Flask/requests + yahoo_finance)").lower() == "y"
except:
    IS_LIVE = True
    CAN_WRITE = False
    print("Can't choose no LiveMode from a shell script defaulting to LIVE_MODE")

    
extracted = {}

def parse_num(num):
    """ number string to float """
    return float(num)

@app.route('/human-io', methods=["POST"])
@crossdomain(origin="*")
def human_io():
    """ basic io test """
    data = flask.request.data.decode(encoding="utf-8", errors="strict")
    json_data = json.loads(data)
    for item in json_data:
        item['Open'] = parse_num(item['Open'])
        item['High'] = parse_num(item['Low'])
        item['Volume'] = parse_num(item['Volume'])
        item['Close'] = parse_num(item['Close'])
        
    return json.dumps({"success":True, "response":(data[:12] + "...")})

def dictconvert(d,form):
    """ converts a dict based on a template """
    cpy = {}
    for key in form:
        name, method = form[key]
        cpy[name] = method(d[key])
    return cpy

def strdateconv(x):
    """ converts str to python date """
    return datetime.datetime.strptime(x, "%Y-%m-%d")

def dateintconv(x):
    """ converts a date to seconds since epoch """
    return int((x - datetime.datetime(1970,1,1)).total_seconds())

def stock_input_conv(extracted, json_data):
    template = { "Close": ["close", lambda x: int(float(x)*100)],"Date": ["date", lambda x: dateintconv(strdateconv(x))]}
    for item in json_data:
        sym = item["Symbol"]
        if(not sym in extracted):
            extracted[sym] = []
        data = extracted[sym]
        data.append(dictconvert(item, template))
    
    #ensure sort
    for sym in extracted:
        extracted[sym] = sorted(extracted[sym],key=lambda x: x["date"])

def tweet_input_conv(json_data):
    template = {"id":["id",lambda x: x], "sentiment":["sentiment",lambda x: x],"time":["date", lambda x: x]}
    for i in range(len(json_data)):
        json_data[i] = dictconvert(json_data[i], template)
    mp = {}
    def filfun(x):
        k = x["date"] // (24 * 3600 * 3)
        if k in mp:
            return False
        mp[k] = True
        return True
    json_data = filter(filfun, json_data)
    #ensure sort
    json_data = sorted(json_data,key=lambda x: x["date"])

    return json_data
    
def save_stock(text, sym):
    if(CAN_WRITE):
        handle = open("files/"+sym+".json", "w")
        handle.write(text)
        handle.close()

def load_stock(sym):
    if(CAN_WRITE):
        handle = open("files/"+sym+".json", "r")
        text = handle.read()
        handle.close()
        return text
    return ""

    
@app.route('/fileout', methods=["POST"])
@crossdomain(origin="*")
def file_outv1():
    data = json.loads(flask.request.data.decode(encoding="utf-8", errors="strict"))
    stocks = {}
    stockReq = data['requests']
    for stock in stockReq:
        stockt = stock.strip()
        if(len(stockt) > 0):
            temp = None
            if(IS_LIVE):
                r = requests.get('http://127.0.0.1:5002/requestStocks?start=2017-3-22&end=2017-4-24&stock='+stockt)
                save_stock(r.text, stockt)
                temp = r.text
            else:
                temp = load_stock(stockt)
            stock_input_conv(stocks, json.loads(temp))

    handle = None
    try:
        handle = open("files/output.json","r")
    except:
        handle = None
    if handle == None:
        return json.dumps([False, "file not found"])
    text = handle.read()
    handle.close()
    text = tweet_input_conv(json.loads(text))
    return json.dumps([True, {"stocks":stocks,"tweets":text}])


@app.route('/datain', methods=["POST"])
@crossdomain(origin="*")
def data_convert_in():
    """ converts input json formatted string into Python object """
    global extracted
    #print(extracted)
    print("returning")
    return json.dumps([True, "All Good!"])

@app.route('/dataout', methods=["GET"])
@crossdomain(origin="*")
def data_convert_out():
    """Converts computed data into a json formatted string"""
    template = { "close": ["close", lambda x: x],"date": ["date", dateintconv]}    
    output = {}
    for sym in extracted:
        data = extracted[sym]
        output[sym] = [dictconvert(item, template) for item in data]
    #print(output)
    print("returning")
    return json.dumps(output)

    


