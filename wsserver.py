from twisted.internet import reactor, task, protocol, defer
from twisted.application import service
from twisted.python import log
from txwebsockets import WebSocketFactory, BasicOperations
from txredis.protocol import Redis, RedisSubscriber
import sys

class HashSubscriber(RedisSubscriber):
    def messageReceived(self, channel, message):
        log.msg("channel %s: message: %s" % (channel, message))
        self._out("%s: %s" % (channel,message))

@defer.inlineCallbacks
def createSubscriber(connection):
    clientCreator = protocol.ClientCreator(reactor, HashSubscriber)
    redis = yield clientCreator.connectTCP('localhost', 6379)
    yield redis.subscribe("special:all")
    connection.on_subscriber_in_place(redis)

@defer.inlineCallbacks
def deleteSubscriber(connection):
    yield connection.redis.transport.loseConnection()

class HashConnector(BasicOperations):
    def on_subscriber_in_place(self,redis):
        # client may already have disconnected before the redis client
        # was connected, so check if we need to destroy it now.
        if (self.connected):
            self.redis = redis
            self.redis._out = self._out
        else:
            deleteSubscriber(self)

    def on_connect(self):
        self.connected = True
        createSubscriber(self)

    def after_connection(self):
        # hack: 1st outgoing frame never reaches the client (weird),
        # so send an empty frame once the connection is set up.
        self._out("")

    def on_close(self, r):
        self.connected = False
        if (self.redis is not None):
            deleteSubscriber(self)

    def on_read(self, line):
        pass

factory = WebSocketFactory(HashConnector)
application = service.Application("hashfeedr")
reactor.listenTCP(8338, factory)
