import json
import sys
from textblob import TextBlob
import unittest

sys.path.append("../")
import nltk_twitter
import run_app

json_twitter = None;

'''
IMPORTANT: Must have Twitter GAthering server running for test_get_tweet to work
RUN: /flask_io_template/run_tweet_server.sh
'''

class NLPTestCase(unittest.TestCase):
	def setUp(self):
		global json_twitter
		json_twitter = json.loads(nltk_twitter.readJSON('../twitter_data_sentiment.json'))

	def test_read_json(self):
		self.assertEqual(json_twitter.get('Donald Trump'), None)

	def test_nlp(self):
		self.assertEqual(nltk_twitter.get_sentiment(TextBlob("Good")), ['Good', 0.7, []])
		self.assertEqual(nltk_twitter.get_sentiment(TextBlob("Bad")), ['Bad', -0.6999999999999998, []])
		self.assertEqual(nltk_twitter.get_sentiment(TextBlob("Neutral"))[0:2], ['Neutral', 0.0])
		# Test edge case
		self.assertEqual(nltk_twitter.get_sentiment(TextBlob(''))[1], 0)
		self.assertEqual(nltk_twitter.get_sentiment(None), [])

	def test_get_tweet(self):
		self.assertEqual(run_app.get_tweet(None, 0, 0), [])
		self.assertEqual(run_app.get_tweet("Donald Trump", None, 0), [])
		# Valid parameters
		twitter_data = run_app.get_tweet("@realDonaldTrump", 1490227200, 1490227200)
		self.assertEqual(len(twitter_data), 5)
		self.assertEqual(twitter_data[0].get('id', ''), '845037368386207746')
		self.assertEqual(twitter_data[0].get('time', 0), 1490227200)
		self.assertEqual(twitter_data[0].get('sentiment', 0), 0.7125)
		self.assertEqual(twitter_data[0].get('noun_phrases', 0), ['industry leaders', 'whitehouse'])

	def test_apply_nlp(self):
		self.assertEqual(nltk_twitter.apply_nlp(''), []);
		self.assertEqual(nltk_twitter.apply_nlp('Not JSON format'), []);

		twitter_data = run_app.get_tweet("@realDonaldTrump", 1490227200, 1490227200)
		twitter_data = nltk_twitter.apply_nlp(json.dumps(twitter_data))
		self.assertEqual(twitter_data[0].get('id', ''), '845037368386207746')
		self.assertEqual(twitter_data[0].get('time', 0), 1490227200)
		self.assertEqual(twitter_data[0].get('sentiment', 0), 0.7125)
		self.assertEqual(twitter_data[0].get('noun_phrases', 0), ['industry leaders', 'whitehouse'])

if __name__ == '__main__':
	unittest.main()
