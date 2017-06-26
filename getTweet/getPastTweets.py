from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from time import sleep
import json
import datetime

# edit these three variables
user = 'realdonaldtrump'
start = datetime.datetime(2017, 3, 23)  # year, month, day
end = datetime.datetime(2017, 4, 21)  # year, month, day

# only edit these if you're having problems
delay = 1  # time to wait on each page load before reading the page
driver = webdriver.Chrome()  # options are Chrome() Firefox() Safari()


# don't mess with this stuff
twitter_data_filename = 'data.json'
days = (end - start).days + 1
id_selector = '.time a.tweet-timestamp'
tweet_selector = 'li.js-stream-item'
text_select = 'tweet-text'
time_selector = 'small.time'
user = user.lower()
ids = []

def set_times(s_month, s_day, e_month, e_day):
    global start
    global end
    start = datetime.datetime(2017, s_month, s_day)
    end = datetime.datetime(2017, e_month, e_day)


def format_day(date):
    day = '0' + str(date.day) if len(str(date.day)) == 1 else str(date.day)
    month = '0' + str(date.month) if len(str(date.month)) == 1 else str(date.month)
    year = str(date.year)
    return '-'.join([year, month, day])

def form_url(since, until):
    p1 = 'https://twitter.com/search?f=tweets&vertical=default&q=from%3A'
    p2 =  user + '%20since%3A' + since + '%20until%3A' + until + 'include%3Aretweets&src=typd'
    return p1 + p2

def increment_day(date, i):
    return date + datetime.timedelta(days=i)

for day in range(days):
    data = {}
    d1 = format_day(increment_day(start, 0))
    d2 = format_day(increment_day(start, 1))
    url = form_url(d1, d2)
    print(url)
    print(d1)
    driver.get(url)
    sleep(delay)
    
    try:
        found_text = driver.find_elements_by_class_name(text_select)
        found_tweets = driver.find_elements_by_css_selector(tweet_selector)
        #found_time = driver.find_elements_by_css_selector(time_selector)
        increment = 10
        
        while len(found_tweets) >= increment:
            print('scrolling down to load more tweets')
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(delay)
            found_tweets = driver.find_elements_by_css_selector(tweet_selector)
            found_text = driver.find_elements_by_class_name(text_select)
            increment += 10
    
    #print('{} tweets found, {} total'.format(len(found_tweets), len(ids)))
        
        for i in range(len(found_tweets)):
            data = {}
            id = found_tweets[i].find_element_by_css_selector(id_selector).get_attribute('href').split('/')[-1]
            t = found_text[i].text
            data['id'] = id
            data['tweet'] = t
            data['time'] = int((start - datetime.datetime(1970,1,1)).total_seconds())
            ids.append(data)
            

    except NoSuchElementException:
        print('no tweets on this day')

    start = increment_day(start, 1)

try:
    with open(twitter_data_filename) as f:
        all_data = ids + json.load(f)
        data_to_write = all_data[:-1]
        print('tweets found on this scrape: ', len(ids))
        print('total tweet count: ', len(data_to_write))
except:
    with open(twitter_data_filename, 'w') as f:
        all_data = ids
        data_to_write = all_data[:-1]
        print('tweets found on this scrape: ', len(ids))
        print('total tweet count: ', len(data_to_write))

with open(twitter_data_filename, 'w') as outfile:
    json.dump(data_to_write, outfile)

print('all done here')
driver.close()
