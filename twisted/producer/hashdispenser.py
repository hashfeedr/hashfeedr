import TwistedTwitterStream
from twisted.internet import reactor
from twisted.python import log
import os, json, urllib, re
import photoservices

class HashDispenser(TwistedTwitterStream.TweetReceiver):
    instances = []

    @classmethod
    def refresh(klass,terms):
        log.msg(klass, ": refresh stream")
        dispenser = klass(terms)

        # when there is an instance currently running, we'll have to make sure
        # it disconnects. however, to make sure we don't lose too much tweets,
        # only disconnect it when the first tweet arrives on the new channel
        if len(klass.instances) > 0:
            dispenser.onConnectionCallback = klass.instances[-1].teardown
        klass.instances.append(dispenser)

        # create a stream for the new dispenser
        usr, pwd = os.environ['TWUSER'], os.environ['TWPASS']
        query = ["track=%s" % ",".join([urllib.quote(s) for s in terms])]
        factory = TwistedTwitterStream._TwitterStreamFactory(dispenser)
        factory.make_header(usr, pwd, "POST", "/1/statuses/filter.json", "&".join(query))
        dispenser.connector = reactor.connectTCP("stream.twitter.com", 80, factory)
        dispenser.factory = factory
        return dispenser

    def __init__(self,terms):
        self.redis = self.__class__.redis
        self.terms = terms
        self.count = 0

    def teardown(self):
        # remove this connection (which will always be the first element)
        self.__class__.instances.pop(0)

        # this method can only be called if a new connection is available,
        # so we're safe to propagate tearing down more connections
        self.fireCallback()

        # abort everything fo' sho'
        self.factory.stopTrying()
        self.connector.disconnect()

    def split(self,text):
        sentences = re.split(r"\s*(\.+\s|,+)\s*", text.lower())
        sentences = [re.split(r"\s*(\s+|http://|\/|\.|\#|\-|\')\s*",x) for x in sentences]

        terms = set()
        for words in sentences:
            for word in words:
                if len(word) < 3:
                    continue
                terms.add(word)
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

    # called after a 200 status. we can assume we're registered to receive
    # all the tracked words after this moment, so can optionally destroy
    # the previously active stream connection
    def connectionMade(self):
        log.msg(self, ": connection made")
        self.fireCallback()

    def fireCallback(self):
        if hasattr(self,"onConnectionCallback"):
            log.msg(self, ": firing onConnectionCallback")
            self.onConnectionCallback()
            delattr(self,"onConnectionCallback")

    def tweetReceived(self,tweet):
        terms = self.split(tweet['text'])
        matches = (self.terms & terms)
        if len(matches) > 0:
            p = self.publishable(tweet)
            for match in matches:
                self.redis.publish('term:%s' % match, p)
        else:
            # can be uncommented to tweak splitting regex etc
            # log.msg("Unmatched terms:", terms)
            pass
