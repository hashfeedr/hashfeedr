import TwistedTwitterStream
from twisted.internet import reactor
from twisted.python import log
import json, urllib, re

class HashDispenser(TwistedTwitterStream.TweetReceiver):
    def __init__(self,redis):
        self.redis = redis
        pass

    def split(self,text):
        sentences = re.split(r"\s*(\.+\s|,+)\s*", text.lower())
        sentences = [re.split(r"\s+",x) for x in sentences]

        terms = []
        for words in sentences:
            for word in words:
                if len(word) < 3:
                    continue
                terms.append(word)
        return terms

    def tweetReceived(self,tweet):
        terms = self.split(tweet["text"])
        self.redis.publish('special:all',json.dumps(tweet))
        pass

def consume(username,password,redis,track=[]):
    consumer = HashDispenser(redis)
    query = ["track=%s" % ",".join([urllib.quote(s) for s in track])]
    tw = TwistedTwitterStream._TwitterStreamFactory(consumer)
    tw.make_header(username, password, "POST", "/1/statuses/filter.json", "&".join(query))
    reactor.connectTCP("stream.twitter.com", 80, tw)
    return consumer
