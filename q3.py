from collectAllTweets import *
import re
import numpy as np
import time
import datetime
import matplotlib.pyplot as plt

FILE_NAME = "q3.txt"
TWEET_FILE_NAME = "all_tweets.json"
hashtags = ["#SB49", "#football", "#MakeSafeHappen", "#brandbowl", "#adbowl"]

def convertStrToTimestamp(time_str):
	return time.mktime(datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").timetuple())

def getAllTweets():
	start_date = datetime.datetime(2015,02,01, 15,00,0)
	#end_date = datetime.datetime(2015,02,01, 16,00,0)
	end_date = datetime.datetime(2015,02,01, 15,10,0)
	time_step = 1 #sec
	fo = open(TWEET_FILE_NAME, "w")
	for hashtag in hashtags:
		all_tweets = collectTweets(hashtag, start_date, end_date, time_step, FILE_NAME)
		for tweets in all_tweets:
			for tweet in tweets:
				fo.write(json.dumps(tweet) + "\n")

	fo.close()


def getTweetsPerSec(hashtag):
	x = []
	y = []
	f = open(FILE_NAME, "r")
	data = f.read().split('\n')
	for line in data:
		contents = re.split(r'\t+', line)
		if len(contents) < 4:
			break
		tag = contents[0].strip()
		if tag == hashtag:
			from_time = contents[1].strip()
			from_time = from_time[from_time.find(":")+2:]
			from_time = convertStrToTimestamp(from_time)
			# to_time = contents[2].strip()
			# to_time = to_time[to_time.find(":")+2:]
			# to_time = convertStrToTimestamp(to_time)
			count = contents[3].strip()
			count = int(count[count.find(":")+2:])
			x.append(from_time)
			y.append(count)
	f.close()

	return zip(x, y)

def getTweetsNumByKw():
	nums = {}
	for hashtag in hashtags:
		nums[hashtag] = 0
	f = open(FILE_NAME, "r")
	data = f.read().split('\n')
	for line in data:
		contents = re.split(r'\t+', line)
		if len(contents) < 4:
			break
		tag = contents[0].strip()
		count = contents[3].strip()
		count = int(count[count.find(":")+2:])
		nums[tag] += count
	x = []
	y = []
	for k, v in nums.iteritems():
		x.append(k)
		y.append(v)
	f.close()
	return zip(x, y)


def plotTweetsNumByKw(kw_num_list):
	x, y = zip(*kw_num_list)
	x = list(x)
	y = list(y)

	data = np.array(y)
	mask = data.nonzero()

	N = len(hashtags)
	ind = np.arange(N)	# the x locations for the groups
	width = 0.35		# the width of the bars

	fig = plt.figure()
	ax2 = fig.add_subplot(111)

	ax2.spines['right'].set_visible(False)
	ax2.spines['top'].set_visible(False)
	ax2.spines['left'].set_visible(False)
	ax2.spines['bottom'].set_visible(False)

	ax2.set_title("Tweet number for each hashtag")
	ax2.set_ylabel("Number")
	ax2.set_xticks(ind+width)
	ax2.set_xticklabels(x)

	#rects = plt.bar(ind+width, y, width, color = 'r')
	rects = plt.bar(ind[mask], data[mask], width, color = 'r')
	autolabel(ax2, rects)
	ax2.set_xlim([0,N])
	plt.show()


def plotTweetsPerSec(xy_list):
	x, y = zip(*xy_list)
	x = list(x)
	y = list(y)

	fig = plt.figure()

	ax1 = fig.add_subplot(111)
	ax1.set_title("Tweets per second")    
	ax1.set_xlabel('Time')
	ax1.set_ylabel("Number")
	ax1.plot(x,y, c='r')

	plt.show()

def autolabel(ax, rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

if __name__ == "__main__":
 	getAllTweets()
	kw_num_list = getTweetsNumByKw()
	plotTweetsNumByKw(kw_num_list)
	xy_list = getTweetsPerSec("#SB49")
	plotTweetsPerSec(xy_list)
