from twisted.internet import reactor, task, protocol, defer
from twisted.application import service
from twisted.python import log
import os, sys
import redis as omg
from producer import hashdispenser, monitor

# twisted likes this
application = service.Application("hashfeedr-producer")

# connect to redis (synchronous for now)
hashdispenser.HashDispenser.redis = omg.Redis()

# make the monitor call class function refresh on the dispenser
# whenever the set of tracking words has changed
m = monitor.Monitor(hashdispenser.HashDispenser.refresh)
