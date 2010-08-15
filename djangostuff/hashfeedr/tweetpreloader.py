import redis

#globals are jummy - this should use some configuration parameter to find the Redis server...
redisclient = redis.Redis()

def getInitialTweets(keyword):
	"""return some initial tweets to display while waiting for the stream to give results, 
	returns empty string if we dont have anything in Redis"""
	
	# get first 5 tweets from the list, they are already jsonified in Redis :)
	tweetlist = redisclient.lrange("ctweets-"+keyword.lower(), 0, 5)
	
	#TODO if list.length == 0 insert a message asking people to tweet more :P
	
	return tweetlist

