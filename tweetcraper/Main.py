import sys
import csv
import json

import pprint
import got
from got.Tweet import tweet_to_dict
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
    return scrape(tc, args.outdir, args.batchsize, args.randsleep)

def arguments():
    parser = argparse.ArgumentParser(description="scrape tweets via twitter website")

    args = {
        "--username": ("tweets by @username", str),
        "--start": ("get tweets after time", str),
        "--end": ("get tweets before time", str),
        "--max": ("get at most max tweets", int),
        "--near": ("get tweets near a location", str),
        "--within": ("get tweets within a distance", str),
        "--outdir": ("specify an output directory", str),
        "--batchsize": ("specify a batch size", int),
        "--randsleep": ("specify a randsleep amount (within 10% of given amount)", int)
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


def is_eq(t1, t2):
    return t1["id_str"] == t2["id_str"] and t2["retweet_id"] == t1["retweet_id"]

def scrape(criteria, outdir=None, batchsize=0, randsleep=0):
    tweets_all = got.TweetManager.getTweets(criteria, outdir=outdir, batchsize=batchsize, randsleep=randsleep)
    return [tweet_to_dict(t) for t in tweets_all]

if __name__ == '__main__':
    pprint.pprint(main())
