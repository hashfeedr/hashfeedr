from twisted.internet import reactor, task, protocol, defer
from twisted.application import service
from twisted.python import log
from twisted.web import util
from txredis.protocol import RedisBase, Redis, RedisSubscriber
import sys, random

# non-pip includes
sys.path.append("twisted/vendor")
from txwebsocket import websocket

class HashSubscriber(RedisSubscriber):
    def messageReceived(self, channel, message):
        log.msg("channel %s: message: %s" % (channel, message))
        self.websocket.write("channel %s: message: %s" % (channel, message))

class HashfeedrWebSocket(websocket.WebSocketHandler):
    def __init__(self,transport,site):
        websocket.WebSocketHandler.__init__(self,transport,site)
        self.connected = True
        self.createSubscriber()

    @defer.inlineCallbacks
    def createSubscriber(self):
        clientCreator = protocol.ClientCreator(reactor, HashSubscriber)
        self.redis = yield clientCreator.connectTCP('localhost', 6379)

        # make the redis subscriber aware of the websocket before it
        # subscribes to the channel
        self.redis.websocket = self
        yield self.redis.subscribe("special:all")

        # client may already have disconnected before the redis client
        # was connected, so check if we need to destroy it now.
        if (not self.connected):
            self.destroyRedisClient()

    @defer.inlineCallbacks
    def destroyRedisClient(self):
        yield self.redis.unsubscribe()
        yield self.redis.transport.loseConnection()

    def write(self,msg):
        self.transport.write(msg)

    def frameReceived(self,frame):
        pass

    def connectionLost(self,reason):
        log.msg("ws: connection lost")
        self.connected = False
        try:
            self.destroyRedisClient()
        except exceptions.AttributeError:
            pass

application = service.Application("hashfeedr")
site = websocket.WebSocketSite(util.Redirect("http://twitter.com/justinbieber"))
site.addHandler("/websession", HashfeedrWebSocket)
reactor.listenTCP(8338, site)