from twisted.internet import reactor, task, protocol, defer
from twisted.python import log
from txredis.protocol import RedisBase, Redis

class Registrar(object):
    @classmethod
    @defer.inlineCallbacks
    def connect(klass,host,port):
        clientCreator = protocol.ClientCreator(reactor,Redis)
        klass.redis = yield clientCreator.connectTCP(host,port)

        # ping redis every 30s for connection keepalive
        klass.keepalive = task.LoopingCall(klass.keepalive)
        klass.keepalive.start(30)
    
    @classmethod
    @defer.inlineCallbacks
    def keepalive(klass):
        log.msg("%s: Keepalive ping" % repr(klass))
        resp = yield klass.redis.ping()
        pass

    @classmethod
    @defer.inlineCallbacks
    def addSocket(klass,websocket):
        yield klass.redis.zincr('terms', websocket.term, 1)

    @classmethod
    @defer.inlineCallbacks
    def removeSocket(klass,websocket):
        yield klass.redis.zincr('terms', websocket.term, -1)

        # ugly: calling redis api straight from here, but easy for now
        klass.redis._mb_cmd('ZREMRANGEBYSCORE', 'terms', '-inf', '0')
        yield klass.redis.getResponse()
