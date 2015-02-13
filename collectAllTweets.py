import urllib
import httplib
import json
import datetime, time

API_KEY = '09C43A9B270A470B8EB8F2946A9369F3'
host = 'api.topsy.com'
url = '/v2/content/tweets.json'
#SB49
#football
#MakeSafeHappen
#brandbowl
#adbowl


def collectTweets(keyword, start_date, end_date, time_step):

	#########   create UNIX timestamps
	logfile = open("search_log.txt", "a+")
	
	all_tweets = []
	# modifiy time
	cur_start_date = start_date
	cur_end_date = cur_start_date + datetime.timedelta(seconds=time_step)
	time_step_modifier = 1.0
	while (cur_end_date <= end_date && cur_start_date < cur_end_date):

		mintime = int(time.mktime(cur_start_date.timetuple()))
		maxtime = int(time.mktime(cur_end_date.timetuple()))
		#########   set query parameters
		params = urllib.urlencode({'apikey' : API_KEY, 'q' : keyword,
                           'mintime': str(mintime), 'maxtime': str(maxtime),
                           'new_only': '1', 'include_metrics':'1', 'limit': 500})

		#########   create and send HTTP request
		req_url = url + '?' + params
		req = httplib.HTTPConnection(host)
		req.putrequest("GET", req_url)
		req.putheader("Host", host)
		req.endheaders()
		req.send('')

		#########   get response and print out status
		resp = req.getresponse()
		#print resp.status, resp.reason

		#########   extract tweets
		resp_content = resp.read()
		ret = json.loads(resp_content)
		tweets = ret['response']['results']['list']
		if len(tweets) < 500:
			time_step_modifier = 1.0
			all_tweets.append(tweets)
			# write into logfile
			line = keyword.ljust(15) + "   From: " + str(cur_start_date) + "   To: " + str(cur_end_date) + "   No. of Results: " + str(len(tweets)) + "\n"
			logfile.write(line)
			print keyword, " From:", cur_start_date, " To:", cur_end_date, " No. of Results:", len(tweets)
			# next time slot
			cur_start_date = cur_end_date
			cur_end_date = cur_start_date + datetime.timedelta(seconds=time_step)
			if cur_end_date > end_date:
				cur_end_date = end_date
		else:
			time_step_modifier *= 2.0
			cur_end_date = cur_start_date + datetime.timedelta(seconds=time_step/time_step_modifier)

	logfile.close()		

	return all_tweets

if __name__ == "__main__":

	#hashtags = ["#SB49", "#football", "#MakeSafeHappen", "#brandbowl", "#adbowl"]
	hashtags = ["#SB49"]
	start_date = datetime.datetime(2015,02,01, 15,45,0)
	end_date = datetime.datetime(2015,02,01, 15,48,0)
	time_step = 30 #sec
	fo = open("tweets.json", "wb")
	for hashtag in hashtags:
		all_tweets = collectTweets(hashtag, start_date, end_date, time_step)
		for tweets in all_tweets:
			for tweet in tweets:
				fo.write(json.dumps(tweet) + "\n")

	fo.close()




	
