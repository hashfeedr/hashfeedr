import redis

def getMostPopularHashes(amount):
	r = redis.Redis()
	try:
		# terms currently being tracked, ordered desc
		return r.zrange("terms",0,amount,True,True)
	except redis.ConnectionError:
		print "Plz start redis :("
		return []
	