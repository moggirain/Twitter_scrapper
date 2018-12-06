import sys
import csv
import json

import pprint
import got

def main():
    if len(sys.argv) > 1:
        query = sys.argv[1]
    pprint.pprint(scrape(query, "02-09-2018", "03-09-2018", 10))

def tweet_to_dict(tweet):
    return {
                "username": tweet.username,
                "id_str": tweet.id,
                "retweeter": tweet.retweeter,
                "retweet_id": tweet.retweet_id,
                "author": tweet.author_id,
                "geo": tweet.geo,
                "content": {
                    "text": tweet.text.encode('utf-8'),
                    #{}"urls": tweet.urls,
                    "hashtags": tweet.hashtags,
                },
                "interactions": {
                    "retweets": tweet.retweets,
                    "mentions": tweet.mentions,
                    "favorites": tweet.favorites
                },
                "permalink": tweet.permalink,
                "date": tweet.date
            }

def is_eq(t1, t2):
    return t1["id_str"] == t2["id_str"] and t2["retweet_id"] == t1["retweet_id"]



def scrape(query, start, end, max_tweets):
    tweet_criteria = got.TweetCriteria().setQuerySearch(query).setMaxTweets(max_tweets)
    tweets_all = got.TweetManager.getTweets(tweet_criteria)
    return [tweet_to_dict(t) for t in tweets_all]



if __name__ == '__main__':
	main()
