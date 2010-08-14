from twisted.internet import reactor, protocol, defer
from txredis.protocol import RedisBase, Redis

class Registrar(object):
    @classmethod
    @defer.inlineCallbacks
    def connect(klass,host,port):
        clientCreator = protocol.ClientCreator(reactor,Redis)
        klass.redis = yield clientCreator.connectTCP(host,port)
    
    @classmethod
    @defer.inlineCallbacks
    def addSocket(klass,websocket):
        yield klass.redis.zincr('terms', websocket.term, 1)

    @classmethod
    @defer.inlineCallbacks
    def removeSocket(klass,websocket):
        yield klass.redis.zincr('terms', websocket.term, -1)
