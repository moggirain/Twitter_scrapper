import sys
import csv

if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

def main():

	def printTweet(descr, t):
		print(descr)
		print("Username: %s" % t.username)
		print("Retweets: %d" % t.retweets)
		print("Text: %s" % t.text)
		print("Mentions: %s" % t.mentions)
		print("Hashtags: %s\n" % t.hashtags)


	## Get tweets by query search
	## Change setMaxTweets(x) function to desired tweet amount

	tweetCriteria = got.manager.TweetCriteria().setQuerySearch('#Education, teacher, student').setSince("2015-05-01").setUntil("2015-09-30").setMaxTweets(5)
	tweetsAll = got.manager.TweetManager.getTweets(tweetCriteria)


	for tweet in tweetsAll:
		#See all Tweet Componenet:
		printTweet("### Result: Get tweets by query search [#Education]", tweet)
		#See just the tweet text:
		print tweet.text, '\n'
		
		#Save tweet components to file
		contentofTw = [tweet.username, tweet.text.encode('utf-8'), tweet.retweets, tweet.mentions, tweet.hashtags]
		dataFile = open('EduTweets.csv', 'a+')
		with dataFile:
			writer = csv.writer(dataFile)
			writer.writerow(contentofTw)

if __name__ == '__main__':
	main()
