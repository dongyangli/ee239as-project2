import datetime
import json

INPUT_FILE_NAME = "all_tweets.json"
OUTPUT_FILE_NAME = "readable_tweets.txt"

def parseTweet():
	f_in = open(INPUT_FILE_NAME, "r")
	f_out = open(OUTPUT_FILE_NAME, "w")
	data = f_in.read().split('\n')
	data = data[0:len(data)-1]
	f_in.close()
	for line in data:
		tweet = json.loads(line)

		date = tweet["firstpost_date"]
		date = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
		text = tweet["tweet"]["text"]
		retweet_count = tweet["tweet"]["retweet_count"]
		user = tweet["author"]["name"]
		output = date + "\n" + text + "\n" + str(retweet_count) + "\n" + user + "\n\n"
		#f_out.write(output)
		print output

	f_out.close()

if __name__ == "__main__":
	parseTweet()