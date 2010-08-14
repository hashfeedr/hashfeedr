import TwistedTwitterStream
from twisted.internet import reactor
import json
import urllib

class HashDispenser(TwistedTwitterStream.TweetReceiver):
    def __init__(self,redis):
        self.redis = redis
        pass

    def tweetReceived(self,tweet):
        self.redis.publish('special:all',json.dumps(tweet))
        pass

def consume(username,password,redis,track=[]):
    consumer = HashDispenser(redis)
    query = ["track=%s" % ",".join([urllib.quote(s) for s in track])]
    tw = TwistedTwitterStream._TwitterStreamFactory(consumer)
    tw.make_header(username, password, "POST", "/1/statuses/filter.json", "&".join(query))
    reactor.connectTCP("stream.twitter.com", 80, tw)
    return consumer
