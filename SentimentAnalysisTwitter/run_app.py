from crossdomain import crossdomain
import datetime
from flask import Flask, request, Response
import json
import requests
import nltk_twitter
from datetime import datetime as ddatetime
try:
	from __init__ import json_file_name
except ImportError:
	json_file_name = 'twitter_data_sentiment.json'
# Date range and search terms
# GET request date, search_team header

app = Flask(__name__)
json_twitter = json.loads('{}')

errors = {
	'400': 'Bad Request',
	'500': 'Internal Server Error'
}

'''
Function handles creation of error Response that is returned back as JSON to request
'''
def gen_error(code, error_msg=None):
	if (error_msg == None):
		error_msg = errors.get(str(code))
	response_data = {
		'code': code,
		'error': error_msg
	}
	return response_data

'''
Function writes JSON data to file
'''
def write_json_file(data):
	with open('./twitter_data_sentiment.json', 'w') as f:
		json.dump(data, f)
		f.close()

'''
Function grabs any data from JSON file, if we have done the query before
'''
def get_existing_data(twitter_handle, start_date, end_date):
	data_cache = json_twitter.get(twitter_handle, [])
	return_data = []
	if (len(data_cache) > 0):
		for tweet in data_cache:
			create_date = tweet.get('created_at', 0)
			if (create_date >= start_date and create_date <= end_date):
				return_data.append(tweet)
	return return_data

'''
Function given a twitter handle and date checks first if the query currently exists in twitter data JSON file
If doesn't, make a new query request

@params  twitter_handle  string value of Twitter handle
@params  date  epoch value of date to query for
@returns  JSON value of sentiment and tweet from Twitter
'''
def get_tweet(twitter_handle, start_date, end_date):
	if (twitter_handle == None or start_date == None or end_date == None):
		return []
	existing_data = get_existing_data(twitter_handle, start_date, end_date)
	# New request for Twitter handle or date, so make request to Twitter Gatherer
	if (len(existing_data) <= 0):
		req_headers = {
			"Accept": "application/json",
		}
		start_date = int(start_date)
		end_date = int(end_date)
		# start_date = ddatetime.fromtimestamp(int(start_date))
		# end_date = ddatetime.fromtimestamp(int(end_date))
		# start_date_array = [start_date.year, start_date.month, start_date.day]
		# end_date_array = [end_date.year, end_date.month, end_date.day]
		# req_body = {
		# 	'start_date': start_date_array,
		# 	'end_date': end_date_array,
		# 	'twitter_handle': twitter_handle
		# }
		req_headers = {
			'Content-Type': 'application/json',
			'Accept': 'application/json'
		}
		# twitter_req = requests.post('http://localhost:5004/fileout', headers = req_headers, data=req_body)
		try:
			twitter_req = requests.post('http://127.0.0.1:5002' + '/fileout', data = json.dumps({"name":"tweets"}))
		except:
			return []
		if (twitter_req.status_code != 200):
			return []
		try:
			twitter_req = twitter_req.json()
			# print(start_date)
			# print(end_date)
			# print(list(map(lambda x: x.get('time', 0), twitter_req[1])))
			# twitter_req = json.loads(str(list(filter(lambda x: (x.get("time", 0) >= start_date and x.get("time", 0) <= end_date), twitter_req[1]))))
			twitter_req = twitter_req[1]
			temp_list = []
			# Check which tweets are within start and end date to return to request origin
			for tweet in twitter_req:
				if (tweet.get('time', 0) >= start_date and tweet.get('time', 0) <= end_date):
					temp_list.append(tweet)
			twitter_req = temp_list
			# twitter_req = json.loads(twitter_req[1], strict=False)
		except ValueError:
			return []
		# Format Twitter datetime to Epoch time
		# for tweet in twitter_req:
		# 	try:
		# 		tweet['created_at'] = ddatetime.strptime(tweet.get('created_at', ''), "%a %b %d %H:%M:%S %z %Y").timestamp()
		# 	except (ValueError):
		# 		tweet['created_at'] = 0
		# Call NLP
		nlp_data = nltk_twitter.apply_nlp(json.dumps(twitter_req))
		print(nlp_data)
		# Update JSON TWitter
		# json_twitter[twitter_handle][date] = nlp_data
		#Write update to file
		# write_json_file(json_twitter)
		return nlp_data
    # Already exists in JSON file
	else:
		return existing_data

@app.route('/request_tweet/', methods=['GET'])
@crossdomain(origin="*")
def grab_tweet():
	# Grab request data from query param
	# /request_tweet/?tweet_date=<number>&twitter_handle=<string>
	start_date = request.args.get('start_date')
	end_date = request.args.get('end_date')
	# Getting Twitter posts from Donald Trump
	twitter_handle = request.args.get('twitter_handle', '@realDonaldTrump')
	# Status code: 400 bad request
	if (start_date == None or end_date == None or twitter_handle == None):
		msg = 'Bad Request: Headers missing tweet_date and twitter_handle'
		return Response(response=json.dumps(gen_error(404, msg)),
						status=400,
						mimetype='application/json')
	# Request to Twitter Gatherer or existing JSON file
	print("Getting data")
	resp_json = get_tweet(twitter_handle, start_date, end_date)
	# print(resp_json)
	return Response(response=json.dumps(resp_json),
					status=200,
					mimetype='application/json')

if __name__ == '__main__':
	# with open('./twitter_data_sentiment.json', 'r') as twitter_sentiment:
	# 	json_twitter = json.load(twitter_sentiment)
	json_twitter = json.loads(nltk_twitter.readJSON(json_file_name))
	app.run(host='localhost', port=5003)
