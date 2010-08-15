from twisted.internet import reactor, task, protocol, defer
from twisted.application import service
from twisted.python import log
from twisted.web import util
from txredis.protocol import RedisBase, Redis, RedisSubscriber
import sys, random

# non-pip includes
from vendor.txwebsocket import websocket

# project imports
from consumer import registrar

class HashSubscriber(RedisSubscriber):
    def messageReceived(self, channel, message):
        # don't waste cycles parsing/compiling json
        self.websocket.write("{ \"tweet\": %s }" % message)

class HashfeedrWebSocket(websocket.WebSocketHandler):
    def __init__(self,transport,request):
        websocket.WebSocketHandler.__init__(self,transport,request)
        self.term = request.postpath[1]

        self.redis = None
        self.connected = True

        self.createSubscriber()
        log.msg("%s: New connection (%s), term: %s" % (repr(self),request,self.term))

    def connectionLost(self,reason):
        log.msg("%s: Connection lost" % repr(self))
        self.connected = False
        if (self.redis is not None):
            self.destroyRedisClient()

    @defer.inlineCallbacks
    def createSubscriber(self):
        clientCreator = protocol.ClientCreator(reactor, HashSubscriber)
        _redis = yield clientCreator.connectTCP('localhost', 6379)

        # make the redis subscriber aware of the websocket before it
        # subscribes to the channel
        _redis.websocket = self
        yield _redis.subscribe("special:all")

        # only set redis when we're completely done
        self.redis = _redis

        # client may already have disconnected before the redis client
        # was connected, so check if we need to destroy it now.
        if (not self.connected):
            self.destroyRedisClient()
        else:
            # ping our registrar
            yield registrar.Registrar.addSocket(self)

    @defer.inlineCallbacks
    def destroyRedisClient(self):
        yield registrar.Registrar.removeSocket(self)
        yield self.redis.unsubscribe()
        yield self.redis.transport.loseConnection()

    def write(self,msg):
        self.transport.write(msg)

    def frameReceived(self,frame):
        pass


application = service.Application("hashfeedr")
site = websocket.WebSocketSite(util.Redirect("http://twitter.com/justinbieber"))
site.addHandler("/ws", HashfeedrWebSocket)

# open up the port after we've established a connection to the registrar
def start_listening(status,site):
    port = 8338
    reactor.listenTCP(port,site)
    log.msg("Now listening on port %d" % port)

def show_exception(err):
    log.msg(repr(err))

# first establish a connection to the registrar
deferred = registrar.Registrar.connect('localhost',6379)
deferred.addCallback(start_listening,site)
deferred.addErrback(show_exception)

