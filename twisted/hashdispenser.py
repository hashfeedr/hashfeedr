from twisted.internet import reactor
import TwistedTwitterStream
import urllib

class HashDispenser(TwistedTwitterStream.TweetReceiver):
    def __init__(self):
        pass

    def tweetReceived(self,tweet):
        print tweet
        pass

def consume(username,password,track=[]):
    consumer = HashDispenser()
    query = ["track=%s" % ",".join([urllib.quote(s) for s in track])]
    tw = TwistedTwitterStream._TwitterStreamFactory(consumer)
    tw.make_header(username, password, "POST", "/1/statuses/filter.json", "&".join(query))
    reactor.connectTCP("stream.twitter.com", 80, tw)
    return consumer
