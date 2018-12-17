import sys
import csv
import json

import pprint
import got
import argparse

def main():
    args = arguments().parse_args()
    tc = got.TweetCriteria(
            username=args.username,
            start=args.start,
            end=args.end,
            maxTweets=args.max,
            near=args.near,
            within=args.within,
            querySearch=" ".join(args.querySearch),
            topTweets=args.topTweets)
    return scrape(tc)

def arguments():
    parser = argparse.ArgumentParser(description="scrape tweets via twitter website")

    args = {
        "--username": ("tweets by @username", str),
        "--start": ("get tweets after time", str),
        "--end": ("get tweets before time", str),
        "--max": ("get at most max tweets", int),
        "--near": ("get tweets near a location", str),
        "--within": ("get tweets within a distance", str)
    }

    for k, var in args.items():
        parser.add_argument(k[1:3], k, help=var[0], type=var[1])

    parser.add_argument("querySearch", 
            help="Get tweets containing the query terms", 
            nargs="+",
            metavar="Q",
            type=str)

    parser.add_argument("-t", "--topTweets", help="get only top tweets", action="store_true")

    return parser


def tweet_to_dict(tweet):
    print(tweet.username, tweet.text)
    res = {
                "username": tweet.username,
                "id_str": tweet.id,
                "retweeter": tweet.retweeter,
                "retweet_id": tweet.retweet_id,
                "author": tweet.author_id,
                "geo": tweet.geo,
                "content": {
                    "text": tweet.text,
                    #{}"urls": tweet.urls,
                    "hashtags": tweet.hashtags
                },
                "interactions": {
                    "retweets": tweet.retweets,
                    "mentions": tweet.mentions,
                    "favorites": tweet.favorites
                },
                "permalink": tweet.permalink,
                "date": tweet.date
            }
    return res

def is_eq(t1, t2):
    return t1["id_str"] == t2["id_str"] and t2["retweet_id"] == t1["retweet_id"]



def scrape(criteria):
    tweets_all = got.TweetManager.getTweets(criteria)
    return [tweet_to_dict(t) for t in tweets_all]

if __name__ == '__main__':
    pprint.pprint(main())
