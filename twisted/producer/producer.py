from twisted.internet import reactor, task, protocol, defer
from twisted.application import service
from twisted.python import log
import os, sys
import redis as omg
from producer import hashdispenser

# connect to redis (synchronous for now)
redis = omg.Redis()

# twisted likes this
application = service.Application("hashfeedr-producer")

# some sample tracking words
track = ['obama']
dispenser = hashdispenser.consume(os.environ['TWUSER'],os.environ['TWPASS'],redis,track)
