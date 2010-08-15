import TwistedTwitterStream
from twisted.internet import reactor
from twisted.python import log
import os, json, urllib, re
import photoservices

class HashDispenser(TwistedTwitterStream.TweetReceiver):
    @classmethod
    def consume(klass,monitor,redis,track=[]):
        consumer = klass(redis)
        usr, pwd = os.environ['TWUSER'], os.environ['TWPASS']
        query = ["track=%s" % ",".join([urllib.quote(s) for s in track])]
        tw = TwistedTwitterStream._TwitterStreamFactory(consumer)
        tw.make_header(usr, pwd, "POST", "/1/statuses/filter.json", "&".join(query))
        reactor.connectTCP("stream.twitter.com", 80, tw)
        consumer.monitor = monitor
        return consumer

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

    def publishable(self,tweet):
        composite = { 'tweet': tweet }
        urls = re.findall(r"http://[^\s,]+",tweet['text'])
        urls = [photoservices.getThumbFromURL(u) for u in urls]
        urls = [u for u in urls if u is not False]

        # only use the first picture, it's enough..
        if len(urls) > 0:
            composite['image'] = urls[0]

        return json.dumps(composite)

    def tweetReceived(self,tweet):
        terms = self.split(tweet['text'])
        p = self.publishable(tweet)
        for monitored in self.monitor.terms:
            if monitored in terms:
                self.redis.publish('term:%s' % monitored,p)
        pass
