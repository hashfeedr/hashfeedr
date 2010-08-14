from twisted.internet import reactor
import hashdispenser
import os, sys

# omg justin is SOO hot <33333 xD!
track = ['justin','bieber']
dispenser = hashdispenser.consume(os.environ['TWUSER'],os.environ['TWPASS'],track)

reactor.run()
