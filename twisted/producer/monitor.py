from twisted.internet import reactor, task, protocol, defer
from twisted.python import log
from txredis.protocol import RedisBase, Redis, RedisSubscriber
from misc import keepalive
import os, sys

class TriggerSubscriber(RedisSubscriber):
    def messageReceived(self, channel, message):
        self.monitor.refresh()

class Monitor(object):
    def __init__(self,callback):
        self.terms = set()
        self.callback = callback
        deferred = self.deferred_initialize()
        deferred.addCallback(self.refresh)

    @defer.inlineCallbacks
    def deferred_initialize(self):
        clientCreator = protocol.ClientCreator(reactor,Redis)

        # passive connection, do an active keepalive
        self.redis = yield clientCreator.connectTCP('localhost', 6379)
        keepalive.KeepAlive.attach(self.redis.ping)

        # subscribers have no timeout
        triggerCreator = protocol.ClientCreator(reactor,TriggerSubscriber)
        _trigger = yield triggerCreator.connectTCP('localhost', 6379)

        # attach the trigger to the pub/sub channel
        _trigger.monitor = self
        yield _trigger.subscribe("producer:trigger")
        self.trigger = _trigger

    @defer.inlineCallbacks
    def refresh(self, *args):
        terms = yield self.redis.zrange('terms', '0', '-1', reverse=True)
        if set(terms) != set(self.terms):
            self.terms = terms
            log.msg("(updated) Tracking words: %s" % repr(self.terms))

            # optionally trigger the callback function
            if self.callback is not None:
                self.callback(terms)
        else:
            log.msg("(same) Tracking words: %s" % repr(self.terms))

class TweetCounter(object):
    def __init__(self,redis):
        self.count = 0
        self.redis = redis
        self.task = task.LoopingCall(self.post)
        self.task.start(1)
        self.redis.delete('stats:tps')
        self.redis.delete('stats:tpm')

    def incr(self):
        self.count += 1
        pass

    @defer.inlineCallbacks
    def post(self):
        cnt = self.count
        self.count = 0

        # add number to list, and subtract popped element
        # when list size is longer than one minute
        num = yield self.redis.push('stats:tps',cnt,tail=True)
        if num > 60:
            popped = yield self.redis.pop('stats:tps',tail=False)
            cnt -= popped

        yield self.redis.incr('stats:tpm',cnt)
