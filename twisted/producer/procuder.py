from twisted.internet import reactor
import hashdispenser
import os, sys
import redis as omg

# connect to redis (synchronous for now)
redis = omg.Redis()

# omg justin is SOO hot <33333 xD!
track = ['justin','bieber']
dispenser = hashdispenser.consume(os.environ['TWUSER'],os.environ['TWPASS'],redis,track)

reactor.run()
