'''
Name: Ben Knutson, Justin Tsang, Weronika Zamilynny
Description:
Version: 0.0.1

'''
### Import Dependencies ###
import json
import nltk
from textblob import TextBlob
from textblob import blob

# Update path to include data packages in current venv
nltk.data.path.append('../venv3/nltk_data/packages/')
nltk.data.path.append('../../venv3/nltk_data/packages/')

### Extract
# READ JSON FILE
def readJSON(filename):
    buffer = "";
    with open(filename) as textfile:
        for line in textfile:
            buffer = buffer + line
    return buffer

'''
Function grabs NLP from tweet and retuns as JSON
'''
# def get_sentiment(tweet_text):
# 	if (not isinstance(tweet_text, TextBlob)):
# 		return {}
# 	# Print polarity of each sentence
# 	for sentence in tweet_text.sentences:
# 		print(sentence)
# 		print(sentence.sentiment.polarity)
# 		print("Getting Nouns:")
# 		print(sentence.noun_phrases)
# 	# Print the entire polarity of sentence(s)
# 	print(tweet_text.sentiment.polarity)
# 	return tweet_text.sentiment.polarity

def write_data(sentiment_json=None, date=None):
	if (date != None and sentiment_json != None):
		output_file = open(date + '.json', 'wra+')
		feeds = []
		try:
			feeds = json.load(output_file)
		except ValueError:
			pass
		feeds.append(sentiment_json)
		output_file.write(json.dumps(feeds))
		output_file.close()

'''
Function given TextBlob extract sentiment of each sentence by calling get_sentiment

@params  tweet_text  TextBlob object
@return  list if sentence is type TextBlob where each index is a list of length 3
		 (index 0: sentence, 1: sentiment, 2: noun_phrases); otherwise empty list
'''
def get_sentiment_by_sentence(tweet_text):
    # Get polarity of each sentence
    sentence_list = []
    if (isinstance(tweet_text, TextBlob)):
	    for sentence in tweet_text.sentences:
	        sentence_data = get_sentiment(sentence)
	        sentence_list.append(sentence_data)
    return sentence_list

'''
Function given TextBlob extract overall sentiment of sentences and all noun_phrases

@params  sentence  TextBlob object
@return  list if sentence is type TextBlob where index 0 is original text, index 1 is sentiment,
		 and index 2 is list of noun_phrases; othwise, empty list
'''
def get_sentiment(sentence):
	sentence_data = []
	if (isinstance(sentence, TextBlob) or isinstance(sentence, blob.Sentence)):
		sentence_data.append(str(sentence))
		sentence_data.append(sentence.sentiment.polarity)
		sentence_data.append(list(sentence.noun_phrases))
	return sentence_data

'''
Function given string Tweet_data converts to JSON and iterates through list and extracts
sentiment and noun_phrases which is appended by calling get_sentiment

@params  tweet_data  JSON in string type
@return  original tweet_data with NLP applied to each tweet
'''
def apply_nlp(tweet_data=None):
	# Load string as JSON
	try:
		tweet_data = json.loads(tweet_data)
	except:
		return []
	# if (not isinstance(tweet_data, list) or len(tweet_data) <= 0):
	# 	return tweet_data
	for i in range(len(tweet_data)):
		# Grab the tweets
		origin_tweet = TextBlob(tweet_data[i]["tweet"])
		# Grab sentiment of original tweet
		overall_sentiment = get_sentiment(origin_tweet)
		sentiment_by_sentence = get_sentiment_by_sentence(origin_tweet)

		#create new JSON object
		if (len(overall_sentiment) == 3):
			tweet_data[i]["sentiment"] = overall_sentiment[1]
			tweet_data[i]["noun_phrases"]=overall_sentiment[2]
			tweet_data[i]["sentence_breakdown"]=sentiment_by_sentence

	# Write to file
	# write_data(date)
	return tweet_data

# if __name__ == "__main__":
# 	string_input = input("Enter text: ")
# 	get_sentiment(TextBlob(string_input))
#     return json.dumps(tweet_data)

#if __name__ == '__main__':
#    data = apply_nlp(open("twitter.json", "r").read())
