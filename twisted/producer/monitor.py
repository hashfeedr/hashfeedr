from twisted.internet import reactor, task, protocol, defer
from twisted.python import log
from txredis.protocol import RedisBase, Redis, RedisSubscriber
import os, sys

class TriggerSubscriber(RedisSubscriber):
    def messageReceived(self, channel, message):
        self.monitor.refresh()

class Monitor(object):
    def __init__(self):
        self.terms = set()
        deferred = self.deferred_initialize()
        deferred.addCallback(self.refresh)

    @defer.inlineCallbacks
    def deferred_initialize(self):
        clientCreator = protocol.ClientCreator(reactor,Redis)
        self.redis = yield clientCreator.connectTCP('localhost', 6379)
        triggerCreator = protocol.ClientCreator(reactor,TriggerSubscriber)
        _trigger = yield triggerCreator.connectTCP('localhost', 6379)

        # attach the trigger to the pub/sub channel
        _trigger.monitor = self
        yield _trigger.subscribe("producer:trigger")
        self.trigger = _trigger

    @defer.inlineCallbacks
    def refresh(self, *args):
        resp = yield self.redis.zrange('terms', '0', '-1', reverse=True)
        self.terms = set(resp)
        log.msg("Updated tracking words: %s" % repr(self.terms))
