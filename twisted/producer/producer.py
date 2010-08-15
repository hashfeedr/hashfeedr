from twisted.internet import reactor, task, protocol, defer
from twisted.application import service
from twisted.python import log
from txredis.protocol import Redis
import os, sys

# project imports
from producer import hashdispenser, monitor

# twisted likes this
application = service.Application("hashfeedr-producer")

@defer.inlineCallbacks
def start(*args):
    clientCreator = protocol.ClientCreator(reactor,Redis)
    redis = yield clientCreator.connectTCP('localhost',6379)
    hashdispenser.HashDispenser.redis = redis

    # keep the number of tweets processed every second
    tc = monitor.TweetCounter(redis)
    hashdispenser.HashDispenser.tweetcounter = tc

    # make the monitor call class function refresh on the dispenser
    # whenever the set of tracking words has changed
    m = monitor.Monitor(hashdispenser.HashDispenser.refresh)

start()
