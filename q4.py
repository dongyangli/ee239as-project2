import json
import numpy as np 
import matplotlib.pyplot as plt
import math
import operator

TWEETS_FILE_NAME = "all_tweets.json"
retweet_nums = {}

def getAllTweets():
	f = open(TWEETS_FILE_NAME, "r")
	data = f.read().split('\n')
	data = data[0:len(data)-1]
	f.close()
	for line in data:
		tweet = json.loads(line)
		tweet_id = tweet["tweet"]["id"]
		retweet_count = tweet["tweet"]["retweet_count"]
		retweet_nums[tweet_id] = retweet_count

def plotRetweetNum():
	x = []
	counts = []
	sorted_nums = sorted(retweet_nums.items(), key=operator.itemgetter(1))
	_, max_retweet_count = sorted_nums[len(sorted_nums)-1]
	# print max_retweet_count
	for k in range(1, max_retweet_count + 1):
		count = 0
		for key in retweet_nums:
			if retweet_nums[key] >= k:
				count += 1
		x.append(k)
		counts.append(count)
	plot(x, counts, "(linear)")
	log_x = []
	log_counts = []
	for i in range(0, len(x)):
		log_x.append(math.log(x[i]))
		log_counts.append(math.log(counts[i]))
	plot(log_x, log_counts, "(log-log)")


def plot(x, y, title):
	fig = plt.figure()

	ax1 = fig.add_subplot(111)
	ax1.set_title("Number of tweets retweeted k times " + title)    
	ax1.set_xlabel('k')
	ax1.set_ylabel("Number")
	ax1.plot(x,y, c='r')

	plt.show()

if __name__ == "__main__":
	getAllTweets()
	plotRetweetNum()


