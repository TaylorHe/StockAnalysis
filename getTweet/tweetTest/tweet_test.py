#Code Goes Here
import sys

#Testing
import unittest

class GetTweetTest(unittest.TestCase):
	
		
	def test_TweetText(self):
		data = open("../getTweet/data.json", 'r')
		self.assertEqual(data, """[{"tweet": "Today I signed the Veterans (OUR HEROES) Choice Program Extension & Improvement Act @ the @WhiteHouse. #S544 \nWatchhttp://45.wh.gov/7x5n53 ", "id": "854793411110588418", "time": 1492560000}, {"tweet": "#BuyAmericanHireAmerican", "id": "854749300114546688", "time": 1492560000}, {"tweet": "Dems failed in Kansas and are now failing in Georgia. Great job Karen Handel! It is now Hollywood vs. Georgia on June 20th.", "id": "854676780527079425", "time": 1492560000}, {"tweet": "Despite major outside money, FAKE media support and eleven Republican candidates, BIG \"R\" win with runoff in Georgia. Glad to be of help!", "id": "854547423464759296", "time": 1492560000}, {"tweet": "A great honor to host PM Paolo Gentiloni of Italy at the White House this afternoon! #ICYMI- Joint Press Conference: http://45.wh.gov/32jE1S ", "id": "855172998747348998", "time": 1492646400}, {"tweet": "We're going to use American steel, we're going to use American labor, we are going to come first in all deals. http://45.wh.gov/7xvM2D ", "id": "855142466034556928", "time": 1492646400}, {"tweet": "Failing @nytimes, which has been calling me wrong for two years, just got caught in a big lie concerning New England Patriots visit to W.H.", "id": "855055509455593472", "time": 1492646400}]""")

if __name__ == '__main__':
	unittest.main()