from tweepy import *
import pandas
import re
from tweepy import OAuthHandler

consumer_key = 'DEnb5VmkPXfQG9K1J3kKpUk1q'
consumer_secret = '069cqcnpoW67w6kv1dmkvh4G8laU68N5AQwspnLTy71KEu7zGU'
access_token = '2798964198-kRaMMl59mrVZYS4orob786AAYj2ZN5g1yzJ8tit'
access_secret = 'eQQVBSkvFiS2i6b6P2bNBwHrusXZSbslWzm9s5CHHqLDy'

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    
    def on_data(self, data):
        print(data)
        return True
    
    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = Stream(auth, l)
    
    #This line filter Twitter Streams to capture data by the keywords
    stream.filter(track=['CS347ISMYLIFE'])

