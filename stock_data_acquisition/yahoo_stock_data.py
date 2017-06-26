# Created by Mark Knapp, Tom Haumersen, and Ayse Akin
# I pledge my honor that I have abided by the Stevens Honor System

# Last updated 5/1/2017

# Stock data acquisition running on Pythonanywhere.
# Takes in three parameters, start, end, and stock.

from flask import Flask
from flask import request
from yahoo_finance import Share
from crossdomain import crossdomain
import json
import datetime
import unittest
import urllib.request
import urllib.parse


app = Flask(__name__)

@app.route('/requestStocks', methods=['GET'])
@crossdomain(origin="*")
def requestStocks():
    if request.method == 'GET':
        startDate = request.args.get('start', '')
        endDate = request.args.get('end', '')
        stock = request.args.get('stock', '')
        parsedStock = getSymbol(stock)
        if not (verifyDateFormat(startDate) and verifyDateFormat(endDate) and verifyDateOrder(startDate, endDate)):
            return json.dumps("")
        return getData(startDate, endDate, parsedStock)

def getData(startDate, endDate, stock):
    yahoo = Share(stock)
    yahoo.get_open()
    return json.dumps(yahoo.get_historical(startDate, endDate))

def verifyDateFormat(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def verifyDateOrder(startDate, endDate):
    return startDate <= endDate

# Unnecessary
def verifyStock(stock):
    try:
        if Share(stock).get_open() == None:
            return False
        else:
            return True
    except:
        return False

# Gets suggested symbol string and pulls symbol from json object
def getSymbol(value):
    result = parseSymbolChecker(getSymbolFromUrl(value))
    jsonObj = json.loads(result)['ResultSet']['Result'][0]['symbol']
    return jsonObj;

# Calls a yahoo finance URL to get recommended stock symbols for a query
def getSymbolFromUrl(string):
    url = 'http://d.yimg.com/autoc.finance.yahoo.com/autoc'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    values = {'query': string,
              'region': '1',
              'lang': 'en',
              'callback': 'SymbolSuggest.ssCallback'}
    headers = {'User-Agent': user_agent}

    data = urllib.parse.urlencode(values)
    data = data.encode('ascii')
    req = urllib.request.Request(url, data, headers)
    with urllib.request.urlopen(req) as response:
       the_page = response.read()
       return the_page

# Parses the response from getSymbolFromUrl to remove extra information and put it in json format
def parseSymbolChecker(string):
    #toRemove = 'YAHOO.Finance.SymbolSuggest.ssCallback('
    response = string.decode("utf-8").split('(',1)[-1]
    response = response[:-2]
    return response



class TestDataVerification(unittest.TestCase):
    def test_dateFormat(self):
        self.assertTrue(verifyDateFormat("2017-04-11"))
        self.assertFalse(verifyDateFormat("2017/04/11"))
        self.assertFalse(verifyDateFormat("2017-13-11"))
        self.assertFalse(verifyDateFormat("2017-11-31"))
        self.assertFalse(verifyDateFormat("-2017-04-11"))

    #verifyDateOrder cannot be called if the dates do not pass the valid format test so valid dates are assumed.
    def test_verifyDateOrder(self):
        self.assertTrue(verifyDateOrder( "2017-04-11","2017-04-12"))
        self.assertTrue(verifyDateOrder( "2017-04-11","2017-04-11"))
        self.assertFalse(verifyDateOrder( "2017-04-12","2017-04-11"))

    def test_stockSymbolQuery(self):
        self.assertEqual(getSymbol("Apple"),"AAPL")
        self.assertEqual(getSymbol("Google"),"GOOG")
        self.assertEqual(getSymbol("Dow Jones"),"^DJI")
        self.assertEqual(getSymbol("Apple"),"AAPL")


if __name__ == '__main__':
      app.run(host='127.0.0.1', port=5002)

