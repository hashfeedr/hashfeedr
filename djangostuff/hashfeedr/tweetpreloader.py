import redis
	
def getInitialTweets(keyword):
	"""return some initial tweets to display while waiting for the stream to give results, 
	returns empty string if we dont have anything in Redis"""
	
	
	redisclient = redis.Redis()

		
	try:
		# get first 5 tweets from the list, they are already jsonified in Redis :)
		tweetlist = redisclient.lrange("itweets-"+keyword.lower(), 0, 5)
	except redis.ConnectionError:
		print "Redis isn't running. Go fix!"
		return []
	
	#TODO if list.length == 0 insert a message asking people to tweet more :P
	
	return tweetlist

