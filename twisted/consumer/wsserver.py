from twisted.internet import reactor, task, protocol, defer
from twisted.application import service
from twisted.python import log
from twisted.web import util
from txredis.protocol import RedisBase, Redis, RedisSubscriber
import sys, random

# non-pip includes
from vendor.txwebsocket import websocket

class HashSubscriber(RedisSubscriber):
    def messageReceived(self, channel, message):
        self.websocket.write("channel %s: message: %s" % (channel, message))

class HashfeedrWebSocket(websocket.WebSocketHandler):
    def __init__(self,transport,request):
        websocket.WebSocketHandler.__init__(self,transport,request)
        self.term = request.postpath[1]
        self.connected = True
        self.createSubscriber()
        log.msg("%s: New connection (%s), term: %s" % (repr(self),request,self.term))

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
        log.msg("%s: Connection lost" % repr(self))
        self.connected = False
        try:
            self.destroyRedisClient()
        except exceptions.AttributeError:
            pass

application = service.Application("hashfeedr")
site = websocket.WebSocketSite(util.Redirect("http://twitter.com/justinbieber"))
site.addHandler("/ws", HashfeedrWebSocket)
reactor.listenTCP(8338, site)
