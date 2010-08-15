from twisted.internet import reactor, task, protocol, defer
from twisted.python import log
from txredis.protocol import RedisBase, Redis
from misc import keepalive

class Registrar(object):
    @classmethod
    @defer.inlineCallbacks
    def connect(klass,host,port):
        clientCreator = protocol.ClientCreator(reactor,Redis)
        klass.redis = yield clientCreator.connectTCP(host,port)

        # ping redis every 30s for connection keepalive
        keepalive.KeepAlive.attach(klass.redis.ping)

    @classmethod
    @defer.inlineCallbacks
    def addSocket(klass,websocket):
        value = yield klass.redis.zincr('terms', websocket.term, 1)
        yield klass.redis.incr('stats:streams')

        # notify the producer when this term was introduced
        if value == 1:
            yield klass.notifyProducer()

    @classmethod
    @defer.inlineCallbacks
    def removeSocket(klass,websocket):
        yield klass.redis.zincr('terms', websocket.term, -1)

        # ugly: calling redis api straight from here, but easy for now
        klass.redis._mb_cmd('ZREMRANGEBYSCORE', 'terms', '-inf', '0')
        removed = yield klass.redis.getResponse()
        yield klass.redis.decr('stats:streams')

        # notify the producer when something changed
        if removed > 0:
            yield klass.notifyProducer()

    @classmethod
    @defer.inlineCallbacks
    def notifyProducer(klass):
        # notify producer of updated tracking terms
        yield klass.redis.publish('producer:trigger', '1')
