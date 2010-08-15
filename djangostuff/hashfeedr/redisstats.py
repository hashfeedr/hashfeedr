import redis

class RedisStats:
	def __init__(self):
		self.r = redis.Redis()
	
	def getMostPopularHashes(self,amount):
		try:
			# terms currently being tracked, ordered desc
			return self.r.zrange("terms",0,amount,True,True)
		except redis.ConnectionError:
			print "Plz start redis :("
			return []

	def getTweetsPerSecond(self):
		try:
			return self.r.get("stats:tps")
		except redis.ConnectionError:
			print "Redis not running :("
			return 0.0
	
	def getStreamCnt(self):
		try:
			return self.r.get("stats:streams")
		except redis.ConnectionError:
			print "Redis not running :("
			return 0