from twisted.internet import reactor
import hashdispenser
import os, sys
import redis as omg

# connect to redis (synchronous for now)
redis = omg.Redis()

# some sample tracking words
track = ['twexit','durftevragen']
dispenser = hashdispenser.consume(os.environ['TWUSER'],os.environ['TWPASS'],redis,track)

reactor.run()
