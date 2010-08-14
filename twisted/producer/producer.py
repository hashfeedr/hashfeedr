from twisted.internet import reactor
import os, sys
import redis as omg
from producer import hashdispenser

# connect to redis (synchronous for now)
redis = omg.Redis()

# some sample tracking words
track = ['twexit','durftevragen']
dispenser = hashdispenser.consume(os.environ['TWUSER'],os.environ['TWPASS'],redis,track)

reactor.run()
