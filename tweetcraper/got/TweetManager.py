import sys, re
import progressbar
import json as jsonlib
from lxml import etree

if sys.version_info[0] < 3:
    import cookielib
    import urllib2 as rq
    from urllib import quote as uquote
else:
    from urllib.parse import quote as uquote
    import http.cookiejar as cookielib
    import urllib.request as rq

from pyquery import PyQuery
from .Tweet import Tweet

# ETPARSER = etree.ETCompatXMLParser()


class TweetManager:
    def __init__(self):
        pass

    @staticmethod
    def getTweets(tweetCriteria, receiveBuffer=None, bufferLength=100, proxy=None):
        bar = progressbar.ProgressBar(max_value=tweetCriteria.maxTweets)
        refreshCursor = ''

        results = []
        resultsAux = []
        cookieJar = cookielib.CookieJar()

        active = True

        while active:
            bar.update(len(results))
            json = TweetManager.getJsonReponse(tweetCriteria, refreshCursor, cookieJar, proxy)
            if len(json['items_html'].strip()) == 0:
                break

            refreshCursor = json['min_position']
            text = json["items_html"]

            pq = PyQuery(text, parser='html')
            tweets = pq('div.js-stream-tweet')

            if len(tweets) == 0:
                break

            for tweetHTML in tweets:
                tpq = PyQuery(tweetHTML, parser='html_fragments')
                tweet = Tweet(tpq)

                results.append(tweet)
                resultsAux.append(tweet)

                if receiveBuffer and len(resultsAux) >= bufferLength:
                    receiveBuffer(resultsAux)
                    resultsAux = []

                if tweetCriteria.maxTweets > 0 and len(results) >= tweetCriteria.maxTweets:
                    active = False
                    break

        if receiveBuffer and len(resultsAux) > 0:
            receiveBuffer(resultsAux)

        return results

    @staticmethod
    def getJsonReponse(tweetCriteria, refreshCursor, cookieJar, proxy):
        url, data = tweetCriteria.url(), tweetCriteria.get_data()
        url = url % (uquote(data), refreshCursor)
        headers = [
                ('Host', "twitter.com"),
                ('User-Agent', "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"),
                ('Accept', "application/json, text/javascript, */*; q=0.01"),
                ('Accept-Language', "de,en-US;q=0.7,en;q=0.3"),
                ('X-Requested-With', "XMLHttpRequest"),
                ('Referer', url),
                ('Connection', "keep-alive")
        ]

        if proxy:
            opener = rq.build_opener(
                    rq.ProxyHandler({'http': proxy, 'https': proxy}), rq.HTTPCookieProcessor(cookieJar))
        else:
            opener = rq.build_opener(rq.HTTPCookieProcessor(cookieJar))
        opener.addheaders = headers

        try:
            response = opener.open(url)
            jsonResponse = response.read()
        except:
            sys.stderr.write("Twitter weird response. Try to see on browser: https://twitter.com/search?q={}&src=typd".format(uquote(data)))
            sys.exit()
            return

        dataJson = jsonlib.loads(jsonResponse.decode())

        return dataJson
